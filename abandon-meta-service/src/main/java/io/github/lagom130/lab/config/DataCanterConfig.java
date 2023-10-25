package io.github.lagom130.lab.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

/**
 * @author lujc
 * @date 2023/10/25.
 */
@Configuration
@ConfigurationProperties(prefix = "snowflake.datacenter.config")
@RefreshScope
@lombok.Data
public class DataCanterConfig {
    private Map<String, Long> serviceNameToDataCenterIdDict;
}
