package io.github.logom130.lab.controller

import io.github.logom130.lab.dto.MessageTemplateDTO
import io.github.logom130.lab.globalResponse.ResultUtils
import io.github130.lab.cat.globalResponse.GlobalResult
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/template")
class TemplateController {

    @PostMapping("")
    fun addOne(dto:MessageTemplateDTO):GlobalResult<Long> {
        println("addOne")
        return ResultUtils.success(200,"success",-1L)
    }

}