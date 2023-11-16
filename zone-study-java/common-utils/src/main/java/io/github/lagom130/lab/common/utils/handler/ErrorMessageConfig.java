package io.github.lagom130.lab.common.utils.handler;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

/**
 * @author lujc
 * @date 2023/9/12.
 */
@Data
@Configuration
@ConfigurationProperties(prefix = "error.code")
public class ErrorMessageConfig {

    private Map<String, String> dictionary;

    private Map<String, String> parameters;

    public String getErrorResultJson(BizErrorCodeEnum errorCodeEnum, String str) {
        if (errorCodeEnum == null) {
            return "";
        }
        String errorCode = errorCodeEnum.name();
        String errorInfo = str;
        String errorInfoFormat = dictionary.getOrDefault(errorCodeEnum.name(), "%s");
        if (errorInfoFormat.contains("%s")) {
            errorInfo = String.format(errorInfoFormat, str);
        }
        return "";
    }

    /**
     * 500 errorInfo
     *
     * @return
     */
    public String get500ErrorInfo() {
        BizErrorCodeEnum errorCodeEnum = BizErrorCodeEnum.INTERNAL_ERROR;
        return dictionary.getOrDefault(errorCodeEnum.name(), BizErrorCodeEnum.INTERNAL_ERROR.name());
    }

    /**
     * 属性缺失
     *
     * @param param
     * @return
     */
    public String getMissingParameterJson(String... param) {
        String parameter = String.join("_", param).toUpperCase();
        return this.formatErrorJson(BizErrorCodeEnum.MISSING_PARAMETER, parameter);
    }

    /**
     * 属性重复
     *
     * @param param
     * @return
     */
    public String getRepeatedParameterJson(String... param) {
        String parameter = String.join("_", param).toUpperCase();
        return this.formatErrorJson(BizErrorCodeEnum.REPEATED_PARAMETER, parameter);
    }

    /**
     * 找不到资源
     *
     * @param param
     * @return
     */
    public String getNotFoundResourceJson(String... param) {
        String parameter = String.join("_", param).toUpperCase();
        return this.formatErrorJson(BizErrorCodeEnum.NOT_FOUND_RESOURCE, parameter);
    }

    /**
     * 属性非法
     *
     * @param param
     * @return
     */
    public String getInvalidParameterJson(String... param) {
        String parameter = String.join("_", param).toUpperCase();
        return this.formatErrorJson(BizErrorCodeEnum.INVALID_PARAMETER, parameter);
    }


    private String formatErrorJson(BizErrorCodeEnum errorCodeEnum, String parameter) {
        return "";
    }
}
