package io.github.lagom130.lab.service;


import com.alibaba.nacos.api.NacosFactory;
import com.alibaba.nacos.api.naming.NamingService;
import com.alibaba.nacos.api.naming.pojo.Instance;
import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.leaf.IDGen;
import io.github.lagom130.lab.leaf.common.PropertyFactory;
import io.github.lagom130.lab.leaf.common.Result;
import io.github.lagom130.lab.leaf.common.ZeroIDGen;
import io.github.lagom130.lab.leaf.snowflake.SnowflakeIDGenImpl;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.temporal.TemporalUnit;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

@Slf4j
@Service
public class SnowflakeService {
    private IDGen idGen;

    private StringRedisTemplate stringRedisTemplate;

    private int workId;

    private static final String SNOWFLAKE_WORK_ID_KEY_PREFIX = "snowflake:workId:";
    private static final Long SNOWFLAKE_WORK_ID_KEY_EXPIRE = 1000*60*60*3L;
    private static final Long SNOWFLAKE_WORK_ID_KEY_EXPIRE_HEART_BEAT = SNOWFLAKE_WORK_ID_KEY_EXPIRE/3;


    public SnowflakeService(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
        boolean flag = false;
        int workId=-1;
        while (!flag) {
            workId++;
            String key = SNOWFLAKE_WORK_ID_KEY_PREFIX+"snowflake:workId:"+workId;
            flag = stringRedisTemplate.opsForValue().setIfAbsent(key, "true", SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS);
        }
        idGen = new SnowflakeIDGenImpl(workId);
        this.workId = workId;
        if(idGen.init()) {
            log.info("Snowflake Service Init Successfully, workId="+workId);
        } else {
            throw new BizException(500, "Snowflake Service Init Fail");
        }
    }

    public Result getId(String key) {
        return idGen.get(key);
    }

    @Scheduled(initialDelay = 100000, fixedRate = 1000*60*60)
    public void heartBeat() {
        stringRedisTemplate.expire("snowflake:workId:"+workId, SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS);
        log.info("snakeflake workId[{}] expire success", workId);
    }
}
