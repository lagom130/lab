package io.github.lagom130.lab.client;

import io.github.lagom130.lab.client.config.ClientDecodeConfiguration;
import io.github.lagom130.lab.client.dto.ApplyDto;
import io.github.lagom130.lab.globalResponse.Result;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(value = "flow-service", configuration = ClientDecodeConfiguration.class)
public interface FlowClient {
    @GetMapping(value = "/snowflakes/global/identifier")
    Long getSnowflakeId();

    @PostMapping("")
    Result<Long> apply(@RequestBody ApplyDto applyDto);
}
