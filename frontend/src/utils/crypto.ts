import CryptoJS from 'crypto-js'

const SECRET_KEY = 'your-secret-key-here' // 在实际生产环境中，这个密钥应该从环境变量中获取

export function encrypt(data: string): string {
  return CryptoJS.AES.encrypt(data, SECRET_KEY).toString()
}

export function decrypt(encryptedData: string): string {
  const bytes = CryptoJS.AES.decrypt(encryptedData, SECRET_KEY)
  return bytes.toString(CryptoJS.enc.Utf8)
} 