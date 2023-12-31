package io.github.lagom130.lab.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.Optional;

/**
 * @author lujc
 * @date 2023/10/30.
 */
@Slf4j
@Component
public class BaseIntercepter implements HandlerInterceptor {
    /**
     * 请求处理前
     * @param request
     * @param response
     * @param handler
     * @return
     * @throws Exception
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        Long userId = Optional.ofNullable(request.getHeader("user-id")).map(Long::valueOf).orElse(null);
        String username = Optional.ofNullable(request.getHeader("user-name")).orElse(null);
        Long orgId = Optional.ofNullable(request.getHeader("org-id")).map(Long::valueOf).orElse(null);
        String orgName = Optional.ofNullable(request.getHeader("org-name")).orElse(null);
        // 获取请求头中的 单位编号 信息
        LoginUserUtils.setLoginUser(new LoginUser(userId, username, orgId, orgName));
        return true;
    }

    /**
     * 请求处理后
     * @param request
     * @param response
     * @param handler
     * @param ex
     * @throws Exception
     */
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

        // 请求完后，需要清空 LoginUserThreadLocal 数据
        // 避免 OOM
        LoginUserUtils.removeUser();
        log.info("-----afterCompletion----LoginUserUtils.remove()");
    }
}
