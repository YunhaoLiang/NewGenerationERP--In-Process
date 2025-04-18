import os
import json
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import Dataset
import torch
from typing import Dict, List
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class OrderModelTrainer:
    """订单模型训练器"""
    
    def __init__(self, model_name: str = "bert-base-chinese"):
        """初始化训练器
        
        Args:
            model_name: 基础模型名称
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=5  # 5个任务类型：order, planning, supply_chain, finance, prediction
        )
        
    def prepare_dataset(self, data_path: str) -> Dataset:
        """准备训练数据集
        
        Args:
            data_path: 训练数据路径
            
        Returns:
            Dataset: 处理后的数据集
        """
        # 加载训练数据
        with open(data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 处理数据
        texts = []
        labels = []
        for item in raw_data:
            texts.append(item['text'])
            # 将任务类型转换为标签
            task_type = item['task_type']
            label_map = {
                'order': 0,
                'planning': 1,
                'supply_chain': 2,
                'finance': 3,
                'prediction': 4
            }
            labels.append(label_map[task_type])
        
        # 创建数据集
        dataset = Dataset.from_dict({
            'text': texts,
            'label': labels
        })
        
        # 分词
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                padding='max_length',
                truncation=True,
                max_length=128
            )
        
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=['text']
        )
        
        return tokenized_dataset
    
    def train(self, train_dataset: Dataset, output_dir: str):
        """训练模型
        
        Args:
            train_dataset: 训练数据集
            output_dir: 模型输出目录
        """
        # 训练参数
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            save_steps=1000,
            evaluation_strategy="steps",
            eval_steps=500
        )
        
        # 数据整理器
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        
        # 计算指标
        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            precision, recall, f1, _ = precision_recall_fscore_support(
                labels, predictions, average='weighted'
            )
            acc = accuracy_score(labels, predictions)
            return {
                'accuracy': acc,
                'f1': f1,
                'precision': precision,
                'recall': recall
            }
        
        # 创建训练器
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
            compute_metrics=compute_metrics
        )
        
        # 开始训练
        trainer.train()
        
        # 保存模型
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
    def generate_training_data(self, output_path: str, num_samples: int = 1000):
        """生成训练数据
        
        Args:
            output_path: 输出文件路径
            num_samples: 样本数量
        """
        # 示例数据模板
        templates = {
            'order': [
                '客户需要订购{quantity}台{product}，配置要求：{config}。交货日期为{date}，地址是{address}。',
                '请处理{quantity}台{product}的订单，配置为{config}，要求{date}前交货到{address}。',
                '新订单：{quantity}台{product}，配置{config}，{date}交货，地址{address}。'
            ],
            'planning': [
                '根据订单生成生产计划，产品{product}，数量{quantity}，交货日期{date}。',
                '请为{quantity}台{product}制定生产计划，确保{date}前完成。',
                '需要生产{quantity}台{product}，请安排生产计划，截止日期{date}。'
            ],
            'supply_chain': [
                '根据生产计划生成{product}的原材料采购计划，数量{quantity}。',
                '请为{quantity}台{product}准备原材料采购方案。',
                '需要采购{quantity}台{product}的原材料，请制定采购计划。'
            ],
            'finance': [
                '根据订单和生产计划生成{product}的财务预算，数量{quantity}。',
                '请为{quantity}台{product}制定财务预算方案。',
                '需要为{quantity}台{product}准备财务预算，请处理。'
            ],
            'prediction': [
                '预测未来{period}的{product}需求趋势。',
                '请分析{product}在未来{period}的市场需求。',
                '需要预测{product}在{period}内的销售情况。'
            ]
        }
        
        # 生成数据
        data = []
        products = ['高性能电脑', '服务器', '工作站']
        configs = [
            'Intel i9处理器，32GB内存，1TB SSD，NVIDIA RTX 4080显卡',
            'AMD Ryzen 9处理器，64GB内存，2TB SSD，NVIDIA RTX 4090显卡',
            'Intel Xeon处理器，128GB内存，4TB SSD，NVIDIA A6000显卡'
        ]
        dates = ['2024-07-01', '2024-08-15', '2024-09-30']
        addresses = [
            '上海市浦东新区张江高科技园区',
            '北京市海淀区中关村科技园',
            '深圳市南山区科技园'
        ]
        periods = ['3个月', '6个月', '1年']
        
        for _ in range(num_samples):
            # 随机选择任务类型
            task_type = np.random.choice(list(templates.keys()))
            template = np.random.choice(templates[task_type])
            
            # 填充模板
            if task_type == 'order':
                text = template.format(
                    quantity=np.random.randint(1, 1000),
                    product=np.random.choice(products),
                    config=np.random.choice(configs),
                    date=np.random.choice(dates),
                    address=np.random.choice(addresses)
                )
            elif task_type in ['planning', 'supply_chain', 'finance']:
                text = template.format(
                    quantity=np.random.randint(1, 1000),
                    product=np.random.choice(products),
                    date=np.random.choice(dates)
                )
            else:  # prediction
                text = template.format(
                    product=np.random.choice(products),
                    period=np.random.choice(periods)
                )
            
            data.append({
                'text': text,
                'task_type': task_type
            })
        
        # 保存数据
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"已生成{num_samples}条训练数据，保存至{output_path}")

if __name__ == "__main__":
    # 创建训练器
    trainer = OrderModelTrainer()
    
    # 生成训练数据
    data_path = "data/training_data.json"
    os.makedirs("data", exist_ok=True)
    trainer.generate_training_data(data_path, num_samples=1000)
    
    # 准备数据集
    dataset = trainer.prepare_dataset(data_path)
    
    # 训练模型
    output_dir = "models/order_classifier"
    os.makedirs("models", exist_ok=True)
    trainer.train(dataset, output_dir)
    
    print("训练完成！模型已保存至", output_dir) 