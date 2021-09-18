#! /bin/bash


# silahkan update variable-variable dibawah ini sesuai kebutuhan
username="Hzz-Hzz"
script_path="/home/"$username"/_script_penting/"
auto_commit_all=1  # 1 atau 0

git_path="/home/"$username"/git/os212/TXT"
script_log_path=$script_path"_checksum_log.txt"



echo $script_log_path


echo ''  >> $script_log_path
echo '==============='  >> $script_log_path
dt=$(date '+%d/%m/%Y %H:%M:%S');  # get current date
echo "$dt" >> $script_log_path
echo ''  >> $script_log_path




FILES="my*.txt my*.sh"
SHA="SHA256SUM"



cd "$git_path"

# mencegah error akibat rebase. Tapi tidak menjamin jika $auto_commit_all != 1
if [ $auto_commit_all == 1 ]; then
    git add . >> $script_log_path
    git commit -m "$dt" >> $script_log_path
else
    git add "$git_path/$SHA.asc" >> $script_log_path
    git add "$git_path/$SHA" >> $script_log_path
    git commit -m "$dt" >> $script_log_path
fi
git pull  >> $script_log_path


string_hasil_cek=$(sha256sum -c $SHA | grep -oP '\S+$')

need_update=0

# mengecek apakah checksum saat ini ada yang invalid atau tidak
while read line 
do
    if [ "$line" != "OK" ]; then
        need_update=1
        echo "$need_update"
        break
    fi
done <<< "$string_hasil_cek"


echo 'need_update='$need_update  >> $script_log_path


# mengecek apakah hasil checksum-nya akan berbeda atau tidak. Menghandle kasus ketika
# kita menambahkan file baru yang formatnya my*.txt (misalnya mynotes.txt)
new_sha=$(sha256sum $FILES)
prev_sha=$(cat $SHA)
if [ "$new_sha" != "$prev_sha" ]; then
    echo 'new_sha and prev_sha is not equal. Updating'  >> $script_log_path
    echo ''  >> $script_log_path
    echo "$new_sha"  >> $script_log_path
    echo ''  >> $script_log_path
    echo "$prev_sha"  >> $script_log_path
    echo ''  >> $script_log_path
    
    need_update=1  # we will update it
    echo 'need_update='$need_update  >> $script_log_path
    echo ''  >> $script_log_path
fi


if (( need_update != 0 )); then
    # mengoutputkan hasil ceksum sebelum diubah ke _checksum_log.txt
    sha256sum -c $SHA >> $script_log_path
    

    
    rm -f $SHA $SHA.asc >> $script_log_path

    sha256sum $FILES > $SHA
    
    sha256sum -c $SHA >> $script_log_path
    echo ''  >> $script_log_path
    
    gpg --output $SHA.asc --armor --sign --detach-sign $SHA >> $script_log_path
    echo ''  >> $script_log_path

    gpg --verify $SHA.asc $SHA >> $script_log_path


    # mencegah error akibat rebase. Tapi tidak menjamin jika $auto_commit_all != 1
    if [ $auto_commit_all == 1 ]; then
        git add . >> $script_log_path
        git commit -m "$dt" >> $script_log_path
    else
        git add "$git_path/$SHA.asc" >> $script_log_path
        git add "$git_path/$SHA" >> $script_log_path
        git commit -m "$dt" >> $script_log_path
    fi
    git push  >> $script_log_path
fi