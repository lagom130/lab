package io.github.lagom130.abandon.canary.service.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Map;

@Component
@FeignClient(value="canary-provider")
public interface CanaryProviderClient {
    @GetMapping("/provider/info/a")
    public Map<String, Object> getInfoA(@RequestParam String username);
}
