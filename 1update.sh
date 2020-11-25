
cd apps/lms_api &&
git reset --hard &&
echo $'Running Git Pull\n' &&
git pull &&
echo $'\nRunning update script: \n' &&
SCRIPT_PATH="./1update_script.sh" &&
source "$SCRIPT_PATH" &&
echo 'Update complete! Please run "bench --site all migrate" '
