const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const sshSync = require('../lib/ssh');


exports.command = 'playbook <file> <inventory>';
exports.desc = 'Run provided playbook with given inventory';
exports.builder = yargs => {
    yargs.options({
        vaultpass: {
            alias: 'vp',
            describe: 'the password to use for ansible vault',
            default: 'matters', // for automated grading
            type: 'string'
        }
    });
};

exports.handler = async argv => {
    const { file, inventory } = argv;

    (async () => {

        if (fs.existsSync(path.resolve(file))
            && fs.existsSync(path.resolve(inventory))) {

            var vaultPasswordFile = ".vault_pass.txt";
            fs.writeFileSync(vaultPasswordFile, argv.vp);

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
