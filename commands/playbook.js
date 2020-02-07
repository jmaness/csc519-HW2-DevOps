const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const sshSync = require('../lib/ssh');


exports.command = 'playbook <file> <inventory> <vault-password-file>';
exports.desc = 'Run provided playbook with given inventory';
exports.builder = yargs => {
    yargs.options({
    });
};


exports.handler = async argv => {
    const { file, inventory, vaultPasswordFile } = argv;

    (async () => {

        if (fs.existsSync(path.resolve(file))
            && fs.existsSync(path.resolve(inventory))
            && fs.existsSync(path.resolve(vaultPasswordFile))) {
            await run(file, inventory, vaultPasswordFile);
        }

        else {
            console.error(`File, inventory, or vault password file don't exist. Make sure to provide path from root of cm directory`);
        }

    })();

};

async function run(file, inventory, vaultPasswordFile) {

    // the paths should be from root of cm directory
    // Transforming path of the files in host to the path in VM's shared folder
    let filePath = '/bakerx/'+ file;
    let inventoryPath = '/bakerx/' +inventory;
    let vaultPasswordPath = '/bakerx/' + vaultPasswordFile;

    console.log(chalk.blueBright('Running ansible script...'));
    let result = sshSync(`/bakerx/cm/run-ansible.sh ${filePath} ${inventoryPath} ${vaultPasswordPath}`, 'vagrant@192.168.33.10');
    if( result.error ) { process.exit( result.status ); }

}
