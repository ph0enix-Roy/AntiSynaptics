# AntiSynaptics

用来从被 Synaptics 蠕虫病毒感染的 exe 文件中提取原始的 Windows™ PE 文件。


## 功能

- 提取被 Synaptics 蠕虫病毒感染的 exe 文件中的原始的 Windows™ PE 文件。
- 原始、单一功能实现。无库依赖、无扫描实现。


## 原理

- Synaptics 蠕虫病毒感染后，会生成带有蠕虫病毒编码的新 PE 文件，原始的 PE 文件被隐藏在新 PE 文件的 RD_RCDATA 资源中。
- 因此，将感染后的 PE 文件中的原始 PE 文件提取出来，就可以恢复原始的 PE 文件。


## 注意事项

1. 仅支持 win32 PE 文件。
2. 未进行大规模测试，但本地测试被感染 PE 文件，提取原始 PE 文件成功。
3. Synaptics 病毒还会感染 Microsoft Excel 文件（以宏病毒形式），本代码仅供抢救有价值的 PE 文件。
4. 仅供学习交流使用。