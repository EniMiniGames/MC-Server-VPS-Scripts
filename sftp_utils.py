import paramiko
import os


class DirectoryUploadingSFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        """
        https://stackoverflow.com/a/19974994/3875151
        Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        """
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def put_dir_approved_list(self, source, target, approved):
        """
        Uploads the contents of the list to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        """
        # Replace forward slash in case of Windows
        approved = [i.replace("\\", "/") for i in approved]

        for item in os.listdir(source):
            full_path = os.path.join(source, item)
            full_path = full_path.replace("\\", "/")
            full_path = full_path[2:] if full_path.startswith("./") else full_path
            # aa/bb/cc.dd
            pass
            if os.path.isfile(full_path) and full_path in approved:
                join = os.path.join(source, item).replace("\\", "/")
                self.put(join, f"{target}/{item}")
            elif not os.path.isfile(full_path):
                self.mkdir(f"{target}/{item}", ignore_existing=True)
                self.put_dir_approved_list(full_path, f"{target}/{item}", approved)
            else:
                pass
                # print("This means file isn't approved")
                # TODO clean up empty dirs later? lol

    def mkdir(self, path, mode=511, ignore_existing=True):
        # Augments mkdir by adding an option to not fail if the folder exists
        try:
            super(DirectoryUploadingSFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise


def put_home_files(transport, files):
    # type: (paramiko.Transport, lis) -> None
    sftp = paramiko.SFTPClient.from_transport(transport)
    slash = os.path.sep

    for f in files:
        try:
            sftp.put(f'.{slash}scripts{slash}{f}', f'./{f}')
        except FileNotFoundError:
            print(f"Error: {f} not found!")
        except Exception as e:
            print(f"{type(e).__name__}:  {str(e)}")
    if sftp:
        sftp.close()
