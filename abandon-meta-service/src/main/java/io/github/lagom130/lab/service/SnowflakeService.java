package io.github.lagom130.lab.service;


import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.leaf.IDGen;
import io.github.lagom130.lab.leaf.common.Result;
import io.github.lagom130.lab.leaf.snowflake.SnowflakeIDGenImpl;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Slf4j
@Service
public class SnowflakeService {
    private IDGen idGen;

    private StringRedisTemplate stringRedisTemplate;

    private int workId;

    private static final String SNOWFLAKE_WORK_ID_KEY_PREFIX = "snowflake:workId:";
    private static final Long SNOWFLAKE_WORK_ID_KEY_EXPIRE = 1000*60*60*3L;

    public SnowflakeService(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
        boolean flag = false;
        int workId=-1;
        while (!flag) {
            workId++;
            String key = SNOWFLAKE_WORK_ID_KEY_PREFIX+workId;
            flag = Boolean.TRUE.equals(stringRedisTemplate.opsForValue().setIfAbsent(key, "true", SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS));
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
        stringRedisTemplate.expire(SNOWFLAKE_WORK_ID_KEY_PREFIX+workId, SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS);
        log.info("snowflake workId[{}] expire success", workId);
    }
}
