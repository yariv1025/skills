# M1 – Improper Credential Usage

## Summary

Security of credentials, API keys, and other secrets in mobile apps. Hardcoded or poorly stored secrets lead to theft and abuse.

## Prevention

- Use platform secure storage (Keychain/Keystore); never hardcode API keys or passwords.
- Prefer short-lived tokens and refresh flows; scope credentials minimally.
- Do not log or expose credentials in UI or backups.

## Examples

### Wrong - Hardcoded API key (Android/Kotlin)

```kotlin
// Attacker can extract from APK with simple strings command
object Config {
    const val API_KEY = "sk-prod-12345abcdef"  // NEVER do this
    const val API_SECRET = "super-secret-key"
}
```

### Right - Secure storage with Android Keystore

```kotlin
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey

// Generate key in Keystore (hardware-backed if available)
fun getOrCreateKey(alias: String): SecretKey {
    val keyStore = KeyStore.getInstance("AndroidKeyStore")
    keyStore.load(null)
    
    return keyStore.getKey(alias, null) as? SecretKey ?: run {
        val keyGenerator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore"
        )
        keyGenerator.init(
            KeyGenParameterSpec.Builder(
                alias,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .build()
        )
        keyGenerator.generateKey()
    }
}

// Store credential securely
fun storeCredential(key: String, value: String) {
    val encryptedPrefs = EncryptedSharedPreferences.create(
        "secure_prefs",
        MasterKey.DEFAULT_MASTER_KEY_ALIAS,
        context,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    encryptedPrefs.edit().putString(key, value).apply()
}
```

### Wrong - Hardcoded secret (iOS/Swift)

```swift
// Extractable from IPA binary
let apiKey = "sk-prod-12345abcdef"
```

### Right - iOS Keychain storage

```swift
import Security

func storeInKeychain(key: String, value: String) -> Bool {
    let data = value.data(using: .utf8)!
    
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: key,
        kSecValueData as String: data,
        kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
    ]
    
    // Delete any existing item
    SecItemDelete(query as CFDictionary)
    
    // Add new item
    let status = SecItemAdd(query as CFDictionary, nil)
    return status == errSecSuccess
}

func getFromKeychain(key: String) -> String? {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: key,
        kSecReturnData as String: true
    ]
    
    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)
    
    guard status == errSecSuccess, let data = result as? Data else {
        return nil
    }
    return String(data: data, encoding: .utf8)
}
```

### Wrong - Credentials in logs

```kotlin
Log.d("Auth", "User logged in with password: $password")
Log.d("API", "Request with key: $apiKey")
```

### Right - Redact sensitive data from logs

```kotlin
Log.d("Auth", "User logged in: ${user.id}")
Log.d("API", "Request sent to ${endpoint}")  // No credentials
```

## Testing

- Scan for hardcoded secrets; verify use of secure storage; check backup and sharing behavior.
