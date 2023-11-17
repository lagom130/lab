package io.github.lagom130.lab.service

import io.github.lagom130.lab.common.core.exception.BizException
import io.github.lagom130.lab.utils.GuidUtil
import jakarta.annotation.Resource
import org.springframework.data.redis.core.StringRedisTemplate
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import java.lang.Boolean
import java.util.concurrent.TimeUnit
import kotlin.Int
import kotlin.Long
import kotlin.String

/**
 * @author lujc
 * @date 2023/10/25.
 */
@Service
class GuidService() {
    private val guidUtil: GuidUtil
    private val workerId: Int
    @Resource
    private lateinit var stringRedisTemplate: StringRedisTemplate

    init {
        var flag = false
        var tempMachineId = -1
        while (!flag) {
            tempMachineId++
            if (tempMachineId >= 32) {
                throw BizException(500, "机器ID超出范围")
            }
            val key = String.format(SNOWFLAKE_ID_KEY_FORMAT, tempMachineId)
            flag = Boolean.TRUE == stringRedisTemplate.opsForValue().setIfAbsent(key, "true", SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS)
        }
        guidUtil = GuidUtil(tempMachineId.toLong())
        workerId = tempMachineId
    }

    fun getId(): Long {
        return guidUtil.getNextNoGeneId()
    }

    fun getId(geneticSource: Long): Long {
        return guidUtil.getNextId(geneticSource)
    }

    @Scheduled(initialDelay = 100000, fixedRate = 1000 * 60 * 60)
    fun heartBeat() {
        stringRedisTemplate.expire(String.format(SNOWFLAKE_ID_KEY_FORMAT, workerId), SNOWFLAKE_WORK_ID_KEY_EXPIRE, TimeUnit.MILLISECONDS)
    }

    companion object {
        private const val SNOWFLAKE_ID_KEY_FORMAT = "snowflake:workerId:%s"
        private const val SNOWFLAKE_WORK_ID_KEY_EXPIRE = 1000 * 60 * 60 * 3L
    }
}
