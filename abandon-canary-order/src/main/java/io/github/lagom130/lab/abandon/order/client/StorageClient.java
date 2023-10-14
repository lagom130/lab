package io.github.lagom130.lab.abandon.order.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient("canary-storage")
public interface StorageClient {
    @PostMapping("/storage/{commodityCode}")
    String deduct(@PathVariable("commodityCode") String commodityCode, @RequestParam int count);
}
