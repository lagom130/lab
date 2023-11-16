package io.github.lagom130.lab.controller

import io.github.lagom130.lab.common.web.utils.ResultUtils
import io.github.lagom130.lab.common.web.vo.GlobalResult
import io.github.lagom130.lab.service.GuidService
import jakarta.annotation.Resource
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

/**
 * @author lujc
 * @date 2023/10/25.
 */
@RestController
class GuidController {
    @Resource
    private lateinit var guidService: GuidService

    @GetMapping(value = ["/guid/next"])
    fun  getGuid(): GlobalResult<Long> {
        return ResultUtils.success(guidService.getId())
    }


    /**
     * 获取通用全局雪花算法id，不含基因片段
     * @return
     */
    @GetMapping(value = ["/guid/next/{geneticSource}"])
    fun getGuid(geneticSource: Long): GlobalResult<Long> {
        return ResultUtils.success(guidService.getId(geneticSource))
    }
}
