package io.github.lagom130.lab.config

/**
 * @author lujc
 * @date 2023/10/30.
 */
class LoginUserUtils {
    companion object {
        var userThreadLocal = ThreadLocal<LoginUser>()

        fun getLoginUser(): LoginUser {
            return userThreadLocal.get()
        }

        fun getLoginUserId(): Long? {
            val user = userThreadLocal.get()
            return if (user?.id != null) {
                user.id
            } else null
        }

        fun setLoginUser(user: LoginUser) {
            userThreadLocal.set(user)
        }

        fun removeUser() {
            userThreadLocal.remove()
        }
    }
}
