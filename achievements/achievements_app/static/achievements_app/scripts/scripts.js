
const SECRET_KEY = 'Ваш_Секретный_Ключ_123!';


function encryptPhoneNumber(phoneNumber) {
    if (typeof phoneNumber !== 'string' || phoneNumber.trim() === '') {
        throw new Error('Неверный формат номера телефона');
    }
    const encrypted = CryptoJS.AES.encrypt(phoneNumber, SECRET_KEY).toString();
    return encrypted;
}


function decryptPhoneNumber(encryptedPhone) {
    if (typeof encryptedPhone !== 'string' || encryptedPhone.trim() === '') {
        throw new Error('Неверный формат зашифрованного номера');
    }
    const bytes = CryptoJS.AES.decrypt(encryptedPhone, SECRET_KEY);
    const decrypted = bytes.toString(CryptoJS.enc.Utf8);
    if (!decrypted) {
        throw new Error('Не удалось расшифровать номер телефона');
    }
    return decrypted;
}

// Функция для сохранения зашифрованного номера в localStorage
function saveEncryptedPhone(phoneNumber) {
    const encrypted = encryptPhoneNumber(phoneNumber);
    localStorage.setItem('encryptedPhone', encrypted);
}

// Функция для получения и расшифровки номера из localStorage
function getDecryptedPhone() {
    const encrypted = localStorage.getItem('encryptedPhone');
    if (!encrypted) {
        return null; // или выбросить ошибку, если нужно
    }
    return decryptPhoneNumber(encrypted);
}

