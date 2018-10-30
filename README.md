# 使用Python压缩图片资源
zip_image批量压缩图片脚步,基于tinypng,支持子文件夹图片压缩,默认并发数10


# 配置环境
#### 安装Python3
        1. 安装homebrew
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
        
        2. 安装Python3
`brew install python3`
        
# 使用方式
##### 执行时需要传递参数:
    1. -i 图片文件夹路径
    2. -o 输出路径
    3. -r 替换原图为压缩后的图片 
    
`python3 zip_image -i 路径`

### 免费申请tinypngKey 
[ https://tinypng.com/developers](https://tinypng.com/developers)