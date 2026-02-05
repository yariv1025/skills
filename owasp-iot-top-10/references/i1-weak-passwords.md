# I1 – Weak, Guessable, or Hardcoded Passwords

## Summary

Default or hardcoded credentials that are easy to guess or cannot be changed. Enables unauthorized device access.

## Prevention

- No default passwords; require user-set or device-unique credentials on first use. Use strong password policy or certificate-based auth. Never ship hardcoded credentials.

## Examples

### Wrong - Hardcoded default password

```c
// Same password on every device - attackable at scale
#define DEFAULT_PASSWORD "admin"
#define DEFAULT_USERNAME "admin"

void setup_device() {
    set_credentials(DEFAULT_USERNAME, DEFAULT_PASSWORD);
}
```

### Right - Unique per-device credentials

```c
// Generate unique password during manufacturing
void setup_device(uint8_t* device_serial) {
    char unique_password[17];
    
    // Derive from device serial + secret key (stored in secure element)
    derive_password(device_serial, FACTORY_SECRET, unique_password);
    
    // Store in secure storage
    secure_store_credential("admin", unique_password);
    
    // Print on device label (or QR code) for user
    print_to_label(unique_password);
}
```

### Right - Force password change on first use

```c
bool is_first_login = true;

int handle_login(const char* user, const char* pass) {
    if (!verify_credentials(user, pass)) {
        return AUTH_FAILED;
    }
    
    if (is_first_login) {
        // Force password change
        return AUTH_CHANGE_PASSWORD_REQUIRED;
    }
    
    return AUTH_SUCCESS;
}

int handle_password_change(const char* old_pass, const char* new_pass) {
    // Enforce password policy
    if (strlen(new_pass) < 12) {
        return ERROR_PASSWORD_TOO_SHORT;
    }
    if (strcmp(old_pass, new_pass) == 0) {
        return ERROR_PASSWORD_SAME;
    }
    
    // Update and mark as changed
    secure_store_credential(current_user, new_pass);
    is_first_login = false;
    return SUCCESS;
}
```

### Wrong - Password stored in plaintext

```c
// Readable from firmware dump
char admin_password[32] = "SuperSecret123";
```

### Right - Hashed password storage

```c
#include <argon2.h>

int set_password(const char* password) {
    uint8_t salt[16];
    uint8_t hash[32];
    
    // Generate random salt
    generate_random(salt, 16);
    
    // Hash with Argon2
    argon2id_hash_raw(
        2,      // iterations
        65536,  // memory (KB)
        1,      // parallelism
        password, strlen(password),
        salt, 16,
        hash, 32
    );
    
    // Store salt and hash
    store_in_secure_element(salt, hash);
    return SUCCESS;
}
```

### IoT password policy

| Requirement | Recommendation |
|-------------|----------------|
| Minimum length | 12+ characters |
| Complexity | Mix of character types |
| Default password | None (unique per device) |
| First login | Force password change |
| Storage | Hashed (Argon2/bcrypt) |
| Recovery | Secure reset mechanism |

## Testing

- Check for default credentials and hardcoded secrets; verify password change and strength.
