package io.github.lagom130.lab.abandon.account.globalResponse;

import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = BizException.class)
    public Result bizExceptionHandler(BizException e) {
        e.printStackTrace();
        return Result.error(e.getErrorCode(), e.getErrorMsg());
    }

    /**
     * 处理其他异常
     *
     */
    @ExceptionHandler(value = Exception.class)
    public Result exceptionHandler( Exception e) {
        e.printStackTrace();
        return Result.error(500, "服务错误");
    }
}
