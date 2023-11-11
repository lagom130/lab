package io.github130.lab.cat.globalResponse

import org.springframework.http.HttpStatus
import org.springframework.http.converter.HttpMessageConversionException
import org.springframework.validation.ObjectError
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class GlobalExceptionHandler {
    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = [BizException::class])
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun bizExceptionHandler(e: BizException): Result<*> {
        return Result(e.errorCode, e.errorMsg, null);
    }

    /**
     * 处理入参校验异常
     *
     */
    @ExceptionHandler(value = [MethodArgumentNotValidException::class])
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun methodArgumentNotValidExceptionHandler(e: MethodArgumentNotValidException): Result<*> {
        val bindingResult = e.bindingResult
        var errorMsg = bindingResult.allErrors.stream().findFirst().map { obj: ObjectError -> obj.defaultMessage }.orElse("参数错误")
        return Result(e.statusCode.value(), errorMsg, null);
    }

    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = [HttpMessageConversionException::class])
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun httpMessageConversionExceptionHandler(e: HttpMessageConversionException?): Result<*> {
        return Result(400, "请求体格式不正确", null)
    }

    /**
     * 处理其他异常
     *
     */
    @ExceptionHandler(value = [Exception::class])
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    fun exceptionHandler(e: Exception?): Result<*> {
        return Result(500, "服务错误", null)
    }
}
