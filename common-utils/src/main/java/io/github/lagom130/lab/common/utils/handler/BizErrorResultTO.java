package io.github.lagom130.lab.common.utils.handler;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 业务代码通用返回体，
 * 原BopMgtService和MinioService接口保留原样
 * 其余业务接口按照此返回体实现
 *
 * @author lujc
 * @date 2023/9/12.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class BizErrorResultTO{
    private String errorCode;
    private String errorInfo;



    /**
     * 通用返回体
     * @param code
     * @param info
     * @return
     * @param <T>
     */
    public static <T> BizErrorResultTO createErrorInstance(String code, String info) {
        return new BizErrorResultTO(code, info);
    }

    /**
     * 500返回体
     * @param info
     * @return
     * @param <T>
     */
    public static <T> BizErrorResultTO create500Instance(String info) {
        return new BizErrorResultTO(BizErrorCodeEnum.INTERNAL_ERROR.name(), info);
    }
}
