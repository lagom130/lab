package io.github.lagom130.lab.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.Resource;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.cache.RedisCacheWriter;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.JdkSerializationRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;

/**
 * @author lujc
 * @date 2023/10/31.
 */
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public RedisConnectionFactory redisConnectionFactory() {
        return new LettuceConnectionFactory();
    }

    @Bean
    public CacheManager cacheManager() {


        return  RedisCacheManager.builder(redisConnectionFactory())
                .cacheDefaults(this.getCacheConfigurationWithTtl(600))
                .withCacheConfiguration("catalog_group", this.getCacheConfigurationWithTtl(300))
                .withCacheConfiguration("catalog", this.getCacheConfigurationWithTtl(1800))
                .withCacheConfiguration("resource", this.getCacheConfigurationWithTtl(1200))
                .withCacheConfiguration("apply", this.getCacheConfigurationWithTtl(1800))
                .build();
    }

    RedisCacheConfiguration getCacheConfigurationWithTtl(long seconds) {
        return RedisCacheConfiguration.defaultCacheConfig()
                .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(new JdkSerializationRedisSerializer()))
//                .disableCachingNullValues() // 不缓存null, 为避免缓存穿透，应该缓存null，故注释掉
                // 缓存数据保存*秒
                .entryTtl(Duration.ofSeconds(seconds));
    }

}
