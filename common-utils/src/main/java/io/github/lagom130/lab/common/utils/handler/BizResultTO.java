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
public class BizResultTO<T>{
    private T response;



    /**
     * 通用返回体
     * @param t
     * @return
     * @param <T>
     */
    public static <T> BizResultTO createInstance(T t) {
        return new BizResultTO(t);
    }

    /**
     * 通用操作成功返回体
     * @return
     * @param <T>
     */
    public static <T> BizResultTO createSuccessInstance() {
        return new BizResultTO(true);
    }
}
