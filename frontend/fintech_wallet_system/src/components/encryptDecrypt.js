
import * as CryptoJS from "crypto-js";
const secretKey = 'your-secret-key';
const handleEncrypt = (input) => {
    if (input) {
        const encrypted = CryptoJS.AES.encrypt(input, secretKey).toString();
        return encrypted;
    }
    else {
        return "";
    }
};

const handleDecrypt = (encryptedData) => {
    if (encryptedData) {
        const decrypted = CryptoJS.AES.decrypt(encryptedData, secretKey).toString(CryptoJS.enc.Utf8);
        return decrypted;
    } else {
        return ""
    }
};

export { handleDecrypt, handleEncrypt };