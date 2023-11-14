package io.github.lagom130.lab.util

import com.baomidou.mybatisplus.annotation.EnumValue
import java.lang.Boolean
import java.lang.reflect.Field
import java.util.*
import kotlin.Enum
import kotlin.IllegalArgumentException
import kotlin.RuntimeException
import kotlin.require

/**
 * @author lujc
 * @date 2023/11/2.
 */
object EnumUtils {
    /**
     * 转换字段需要注解@com.baomidou.mybatisplus.annotation.EnumValue
     * 没有对应枚举返回null
     * @param value
     * @param enumClass
     * @return
     * @param <E>
    </E> */
    fun <E : Enum<E>?, T> parse(value: T, enumClass: Class<E>): E {
        require(!Objects.isNull(enumClass)) { "enumClass cannot be null" }
        val field = findEnumKeyFiled(enumClass)
                .orElseThrow {
                    IllegalArgumentException(
                            enumClass.toString() + " must have a filed with the annotation " + EnumValue::class.java)
                }
        field.setAccessible(Boolean.TRUE)
        return Arrays.stream(enumClass.getEnumConstants())
                .filter { enumConstant: E? ->
                    try {
                        return@filter field[enumConstant] == value
                    } catch (e: IllegalAccessException) {
                        throw RuntimeException(e)
                    }
                }
                .findFirst()
                .orElse(null)
    }

    private fun <E : Enum<E>?> findEnumKeyFiled(enumClass: Class<E>): Optional<Field> {
        return Arrays.stream(enumClass.getDeclaredFields())
                .filter { field: Field -> Objects.nonNull(field.getDeclaredAnnotation(EnumValue::class.java)) }
                .findFirst()
    }
}
