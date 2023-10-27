POST http://ccm-prod.wingconn.cn/apps/500001014/envs/DEV/clusters/default/namespaces/dds/item

{"tableViewOperType":"create","key":"testK","value":"testV","comment":"testC","addItemBtnDisabled":true}

PUT http://ccm-prod.wingconn.cn/apps/500001014/envs/DEV/clusters/default/namespaces/dds/item

{"id":21948,"namespaceId":1594,"key":"testK","value":"testVU","comment":"testCU","lineNum":2,"dataChangeCreatedBy":"datamidd","dataChangeLastModifiedBy":"datamidd","dataChangeCreatedTime":"2021-11-25T14:04:58.000+0800","dataChangeLastModifiedTime":"2021-11-25T14:04:58.000+0800","tableViewOperType":"update"}

GET http://ccm-prod.wingconn.cn/apps/500001014/envs/DEV/clusters/default/namespaces/dds/items

DELETE http://ccm-prod.wingconn.cn/apps/500001014/envs/DEV/clusters/default/namespaces/dds/items/21948

发布
POST http://ccm-prod.wingconn.cn/apps/301100005002/envs/DEV/clusters/default/namespaces/application/releases
