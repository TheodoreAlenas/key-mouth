
const deployConf = {
    output: 'export',
    //skipTrailingSlashRedirect: true,
    distDir: '../git-ignores/front-static-serve.gitig',
    basePath: '/key-mouth'
}

const deployEnv = process.env.KEYMOUTH_DEPLOY

const nextConfig = deployEnv === undefined ? {} : deployConf

module.exports = nextConfig
