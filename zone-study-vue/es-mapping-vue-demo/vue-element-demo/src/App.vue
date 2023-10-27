<template>
    <div id="app">
        <h5> es Mapping input</h5>
        <el-input
                type="textarea"
                :rows="2"
                placeholder="请输入内容"
                v-model="esMappingData">
        </el-input>
        <h5> Tree input</h5>
        <el-input
                type="textarea"
                :rows="2"
                placeholder="请输入内容"
                v-model="treeData">
        </el-input>
        <h5> ES Mapping</h5>
        <p>{{esMappingData}}</p>

        <h5> Tree data</h5>
        <div>
            <el-tree :data="JSON.parse(treeData)">
                <span slot-scope="{ node, data }">
                    <el-input v-model="data.name"></el-input>
                    <el-input v-model="data.type"></el-input>
                    <el-input v-model="data.paramConfig.toString()"></el-input>
                </span>
            </el-tree>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                esMappingData: "{\"mapping\":{\"_doc\":{\"properties\":{\"foo\":{\"type\":\"text\",\"fields\":{\"keyword\":{\"type\":\"keyword\",\"ignore_above\":256}}},\"message\":{\"type\":\"text\",\"analyzer\":\"english\"},\"post_date\":{\"type\":\"date\"},\"user\":{\"type\":\"keyword\"}}}}}"
            }
        },
        methods: {

            /**
             * es mapping data's properties convert
             * property's key equals child's name value
             * property's properties equals child's children
             * property's parameter except properties and type is child's paramConfig
             *
             * @param properties
             * @returns {string}
             */
            propertiesConvert(properties) {
                let array = []
                for (let param in properties) {
                    let type = ''
                    let paramConfig = {}
                    let children = []
                    for (let p in properties[param]) {
                        if (p === 'properties') {
                            children = this.propertiesConvert(properties[param][p])
                        } else if (p === 'type') {
                            type = properties[param][p];
                        } else {
                            paramConfig[p] = properties[param][p];
                        }
                    }
                    array.push({
                        name: param,
                        type: type,
                        paramConfig: paramConfig,
                        children: children
                    })
                }
                return JSON.stringify(array)
            },

            /**
             * tree data's children convert
             *
             * @param properties
             * @returns {string}
             */
            childrenConvert(children) {
                let obj = {}
                children.forEach(child => {
                    let key = child['name']
                    let value = {
                        type: child['type']
                    }
                    for (let confKey in child['paramConfig']) {
                        value[confKey] = child['paramConfig'][confKey]
                    }
                    if (child['children'] && child.length > 0) {
                        value['properties'] = this.childrenConvert(child['children'])
                    }
                    obj[key] = value
                })
                return obj
            }
        },
        computed: {
            treeData: {
                get: function () {
                    return this.propertiesConvert(JSON.parse(this.esMappingData)['mapping']['_doc']['properties'])
                },
                set: function (newValue) {
                    this.esMappingData = JSON.stringify({
                        mapping: {
                            _doc: {
                                properties: this.childrenConvert(JSON.parse(newValue))
                            }
                        }
                    })
                }
            }
        }
    }
</script>

<style>
    #app {
        font-family: Helvetica, sans-serif;
        text-align: center;
    }
</style>
