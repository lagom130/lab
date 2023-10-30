package io.github.lagom130.lab.globalResponse;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageConversionException;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = BizException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result bizExceptionHandler(BizException e) {
        return Result.error(e.getErrorCode(), e.getErrorMsg());
    }

    /**
     * 处理入参校验异常
     *
     */
    @ExceptionHandler(value = MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result methodArgumentNotValidExceptionHandler(MethodArgumentNotValidException e) {
        BindingResult bindingResult = e.getBindingResult();
        return Result.error(e.getStatusCode().value(),
                bindingResult.getAllErrors().stream().findFirst().map(DefaultMessageSourceResolvable::getDefaultMessage).orElse("参数错误"));
    }

    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = HttpMessageConversionException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Result httpMessageConversionExceptionHandler(HttpMessageConversionException e) {
        return Result.error(400, "请求体格式不正确");
    }

    /**
     * 处理其他异常
     *
     */
    @ExceptionHandler(value = Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public Result exceptionHandler( Exception e) {
        log.error("系统异常", e);
        return Result.error(500, "服务错误");
    }
}
