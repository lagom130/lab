package io.github.lagom130.lab.service;

import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.util.SnowFlakeUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * @author lujc
 * @date 2023/10/25.
 */
@Slf4j
@Service
public class SnowflakeIdentifierService {
    private SnowFlakeUtil snowFlakeUtil;

    private StringRedisTemplate stringRedisTemplate;

    private int datacenterId = 0;
    private int machineId;

    private static final String SNOWFLAKE_ID_KEY_FORMAT = "snowflake:datacenterId:{}:machineId:{}";
    private static final Long SNOWFLAKE_WORK_ID_KEY_EXPIRE = 1000*60*60*3L;

    public SnowflakeIdentifierService(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
        boolean flag = false;
        int tempMachineId=-1;
        while (!flag) {
            tempMachineId++;
            if(tempMachineId>=32) {
                throw new BizException(500,"机器ID超出范围");
            }
            String key = String.format(SNOWFLAKE_ID_KEY_FORMAT, datacenterId, tempMachineId);
            flag = Boolean.TRUE.equals(stringRedisTemplate.opsForValue().setIfAbsent(key, "true", SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS));
        }
        snowFlakeUtil = new SnowFlakeUtil(datacenterId,machineId);
        this.machineId = tempMachineId;
    }

    public long getId() {
        return snowFlakeUtil.getNextId();
    }

    @Scheduled(initialDelay = 100000, fixedRate = 1000*60*60)
    public void heartBeat() {
        stringRedisTemplate.expire(String.format(SNOWFLAKE_ID_KEY_FORMAT, datacenterId, machineId), SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS);
        log.info("snowflake:datacenterId:{}:machineId:{} expire success", datacenterId,machineId);
    }
}
