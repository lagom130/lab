package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.SnowFlakeMachineRegisterService;
import io.github.lagom130.lab.service.SnowflakeIdentifierService;
import io.github.lagom130.lab.vo.SnowFlakeMetaVO;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

/**
 * @author lujc
 * @date 2023/10/25.
 */
@Slf4j
@RestController
public class SnowflakeIdentifierController {
    @Resource
    SnowflakeIdentifierService snowflakeIdentifierService;
    @Resource
    SnowFlakeMachineRegisterService snowFlakeMachineRegisterService;

    /**
     * 获取通用全局雪花算法id，datacenterId为0，由本组件生成ID
     * @return
     */
    @GetMapping(value = "/snowflakes/global/identifier")
    public Result<Long> getSnowflakeId() {
        return new Result<Long>().success(snowflakeIdentifierService.getId());
    }

    /**
     * 获取雪花算法机器ID，根据serviceName分配datacenterId和machineId,
     * 只确保workId的唯一，由组件自己使用工具类生成ID，减少网络的影响
     * @param serviceName
     * @return
     */
    @GetMapping(value = "/snowflakes/services/{serviceName}/machines")
    public Result<SnowFlakeMetaVO> getMachineId(@PathVariable("serviceName") String serviceName) {
        return new Result<SnowFlakeMetaVO>().success(snowFlakeMachineRegisterService.getMachineId(serviceName));
    }

    /**
     * machineId续约，各组件定时调用
     * @param serviceName
     * @param machineId
     * @return
     */
    @PostMapping(value = "/snowflakes/services/{serviceName}/machines/{machineId}")
    public Result<Void> renewMachineId(@PathVariable("serviceName") String serviceName, @PathVariable("machineId") Long machineId) {
        snowFlakeMachineRegisterService.renewMachineId(serviceName, machineId);
        return new Result<Void>().success();
    }
}
