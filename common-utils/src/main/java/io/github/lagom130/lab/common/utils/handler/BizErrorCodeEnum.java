package io.github.lagom130.lab.common.utils.handler;

/**
 * 业务返回体错误编码
 *
 * @author lujc
 * @date 2023/9/12.
 */
public enum BizErrorCodeEnum {
    EMPTY_REQUEST_BODY,
    INVALID_REQUEST_BODY,
    REPEATED_PARAMETER,
    MISSING_PARAMETER,
    INVALID_PARAMETER,
    NOT_FOUND_RESOURCE,
    INVALID_FORMAT,
    DEPENDENCY_VIOLATION_PARAMETER,
    INTERNAL_ERROR,
    BAD_REQUEST,
    ;
}
