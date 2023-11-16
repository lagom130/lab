package io.github.lagom130.lab.config

import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor
import com.baomidou.mybatisplus.extension.plugins.inner.OptimisticLockerInnerInterceptor
import org.mybatis.spring.annotation.MapperScan
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

/**
 * @author lujc
 * @date 2023/11/13.
 */
@Configuration
@MapperScan("io.github.lagom130.lab.mapper")
class MybatisConfig {
    @Bean
    fun mybatisPlusInterceptor(): MybatisPlusInterceptor {
        val interceptor = MybatisPlusInterceptor()
        interceptor.addInnerInterceptor(OptimisticLockerInnerInterceptor())
        return interceptor
    }
}
