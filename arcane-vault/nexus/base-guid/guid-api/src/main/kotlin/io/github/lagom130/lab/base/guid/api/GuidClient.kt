package io.github.lagom130.lab.base.guid.api

import io.github.lagom130.lab.common.core.vo.GlobalResult
import org.springframework.cloud.openfeign.FeignClient
import org.springframework.web.bind.annotation.GetMapping

@FeignClient(value = "base-guid-service", configuration = [ClientDecodeConfiguration::class])
interface GuidClient {
    @GetMapping(value = ["/guid/next"])
    fun  getGuid(): GlobalResult<Long>


    /**
     * 获取通用全局雪花算法id，不含基因片段
     * @return
     */
    @GetMapping(value = ["/guid/next/{geneticSource}"])
    fun getGuid(geneticSource: Long): GlobalResult<Long>
}
