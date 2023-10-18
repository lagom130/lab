package io.github.lagom130.lab.common.utils.enums.utils;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Objects;
import java.util.Optional;

/**
 * @author lujc
 * @date 2023/9/11.
 */
public class EnumUtils {

    /**
     * 忽略大小写转换枚举
     * 转换字段需要注解@EnumKey
     * 没有对应枚举返回null
     * @param value
     * @param enumClass
     * @return
     * @param <E>
     */
    public static <E extends Enum<E>> E parseIgnoreCase(String value, Class<E> enumClass) {
        if(Objects.isNull(value)) {
            return null;
        }
        if(Objects.isNull(enumClass)) {
            throw new IllegalArgumentException("enumClass cannot be null");
        }
        Field field = findEnumKeyFiled(enumClass)
                .orElseThrow(() -> new IllegalArgumentException(
                        enumClass + " must have a filed with the annotation " + EnumKey.class));
        field.setAccessible(Boolean.TRUE);
        return Arrays.stream(enumClass.getEnumConstants())
                .filter(enumConstant -> {
                    try {
                        return value.equalsIgnoreCase(String.valueOf(field.get(enumConstant)));
                    } catch (IllegalAccessException e) {
                        throw new RuntimeException(e);
                    }
                })
                .findFirst()
                .orElse(null);
    }

    private static <E extends Enum<E>> Optional<Field> findEnumKeyFiled(Class<E> enumClass) {

        return Arrays.stream(enumClass.getDeclaredFields())
                .filter(field -> Objects.nonNull(field.getDeclaredAnnotation(EnumKey.class)))
                .findFirst();

    }
}
