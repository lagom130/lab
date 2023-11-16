package io.github.lagom130.lab.abandon.storage.service;

import io.github.lagom130.lab.abandon.storage.entity.Storage;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.transaction.annotation.Transactional;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
public interface IStorageService extends IService<Storage> {
    void deduct(String commodityCode, int count);
}
