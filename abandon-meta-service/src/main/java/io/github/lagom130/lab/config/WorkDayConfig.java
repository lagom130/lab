package io.github.lagom130.lab.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

@Configuration
@ConfigurationProperties(prefix = "workday.config")
@RefreshScope
@lombok.Data
public class WorkDayConfig {
    private Map<Integer, Boolean> dayOfWeekIsWorkdayDict;
    private Map<String, Boolean> customWorkdayDict;
}
