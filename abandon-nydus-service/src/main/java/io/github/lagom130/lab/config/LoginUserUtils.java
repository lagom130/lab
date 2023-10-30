package io.github.lagom130.lab.config;

/**
 * @author lujc
 * @date 2023/10/30.
 */
public class LoginUserUtils {

    //线程变量，存放user实体类信息，即使是静态的与其他线程也是隔离的
    private static ThreadLocal<LoginUser> userThreadLocal = new ThreadLocal<LoginUser>();

    //从当前线程变量中获取用户信息
    public static LoginUser getLoginUser() {
        LoginUser user = userThreadLocal.get();
        return user;
    }

    /**
     * 获取当前登录用户的ID
     * 未登录返回null
     *
     * @return
     */
    public static Long getLoginUserId() {
        LoginUser user = userThreadLocal.get();
        if (user != null && user.getId() != null) {
            return user.getId();
        }
        return null;
    }

    //为当前的线程变量赋值上用户信息
    public static void setLoginUser(LoginUser user) {
        userThreadLocal.set(user);
    }

    //清除线程变量
    public static void removeUser() {
        userThreadLocal.remove();
    }
}
