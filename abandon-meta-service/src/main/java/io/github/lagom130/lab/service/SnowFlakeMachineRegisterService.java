package io.github.lagom130.lab.service;

import io.github.lagom130.lab.config.DataCanterConfig;
import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.vo.SnowFlakeMetaVO;
import jakarta.annotation.Resource;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.concurrent.TimeUnit;

/**
 * @author lujc
 * @date 2023/10/25.
 */
@Service
public class SnowFlakeMachineRegisterService {
    @Resource
    private DataCanterConfig dataCanterConfig;
    @Resource
    private StringRedisTemplate stringRedisTemplate;

    private static final String SNOWFLAKE_ID_KEY_FORMAT = "snowflake:datacenterId:{}:machineId:{}";

    private static final Long SNOWFLAKE_WORK_ID_KEY_EXPIRE = 1000*60*60*3L;

    public SnowFlakeMetaVO getMachineId(String serviceName) {
        Long datacenterId = dataCanterConfig.getServiceNameToDataCenterIdDict().getOrDefault(serviceName, null);
        if(datacenterId == null) {
            throw new BizException(500, "服务名错误或未配置");
        }
        boolean flag = false;
        Long tempMachineId=-1L;
        while (!flag) {
            tempMachineId++;
            if(tempMachineId>=32) {
                throw new BizException(500,"机器ID超出范围");
            }
            String key = String.format(SNOWFLAKE_ID_KEY_FORMAT, datacenterId, tempMachineId);
            flag = Boolean.TRUE.equals(stringRedisTemplate.opsForValue().setIfAbsent(key, "true", SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS));
        }
        return SnowFlakeMetaVO.builder().datacenterId(datacenterId).machineId(tempMachineId).build();
    }

    /**
     * machineId续约，各组件定时调用
     * @param serviceName
     * @param machineId
     * @return
     */
    public void renewMachineId(String serviceName, Long machineId) {
        Long datacenterId = dataCanterConfig.getServiceNameToDataCenterIdDict().getOrDefault(serviceName, null);
        if(datacenterId == null) {
            throw new BizException(500, "服务名错误或未配置");
        }
        stringRedisTemplate.expire(String.format(SNOWFLAKE_ID_KEY_FORMAT, datacenterId, machineId), SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS);
    }
}
