package io.github.lagom130.abandon.canary.controller;

import io.github.lagom130.abandon.canary.service.client.CanaryProviderClient;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.loadbalancer.LoadBalancerClient;
import org.springframework.cloud.loadbalancer.cache.LoadBalancerCacheManager;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/consumer")
public class ConsumerController {
    @Resource
    private RestTemplate restTemplate;

    @Resource
    private LoadBalancerClient loadBalancerClient;

    @Value("${spring.application.name}")
    private String appName;

    @Resource
    private CanaryProviderClient providerClient;

    @GetMapping("/echo/app-name")
    public String echo() {
        ServiceInstance serviceInstance = loadBalancerClient.choose("canary-provider");
        String url = String.format("http://%s:%s/provider/echo/%s", serviceInstance.getHost(), serviceInstance.getPort(), appName);
        System.out.println("request url:" + url);
        String result = restTemplate.getForObject(url, String.class);
        return result;
    }

    @GetMapping("/info")
    public Map<String, Object> getInfo(@RequestParam String username) {
         return providerClient.getInfoA(username);
    }
}
