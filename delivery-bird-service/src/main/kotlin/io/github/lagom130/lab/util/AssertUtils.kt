package io.github.lagom130.lab.util

import java.util.*
import java.util.function.BiPredicate
import java.util.function.Predicate
import java.util.function.Supplier

/**
 * @author lujc
 * @date 2023/11/1.
 */
object AssertUtils {
    fun <T, E : RuntimeException> isTrue(t: T, verifier: Predicate<T>, exSupplier: Supplier<E>) {
        // 断言结果
        val asserted = verifier.test(t)
        // 断言未通过
        if (!asserted) throw exSupplier.get()
    }

    fun <T, E : RuntimeException> isTrue(caller: T, reference: T, verifier: BiPredicate<T, T>, exSupplier: Supplier<E>) {
        // 断言结果
        val asserted = verifier.test(caller, reference)
        // 断言未通过
        if (!asserted) throw exSupplier.get()
    }

    /**********************************************以下为断言时的常用方法,提供静态方法引用  */ // 对象为空
    fun <T> isNull(t: T): Boolean {
        return Objects.isNull(t)
    }

    // 对象非空
    fun <T> isNotNull(t: T): Boolean {
        return !isNull(t)
    }

    // 比较后相等
    fun <T : Comparable<T>?> isEq(caller: T, reference: T): Boolean {
        return caller!!.compareTo(reference) == 0
    }

    // 比较后大于
    fun <T : Comparable<T>?> isGt(caller: T, reference: T): Boolean {
        return caller!!.compareTo(reference) == 1
    }

    // 比较后大于等于
    fun <T : Comparable<T>?> isGe(caller: T, reference: T): Boolean {
        return caller!!.compareTo(reference) >= 0
    }

    // 比较后小于
    fun <T : Comparable<T>?> isLt(caller: T, reference: T): Boolean {
        return caller!!.compareTo(reference) == -1
    }

    // 比较后小于等于
    fun <T : Comparable<T>?> isLe(caller: T, reference: T): Boolean {
        return caller!!.compareTo(reference) <= 0
    }
}
