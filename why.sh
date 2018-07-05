error_log() {
	error="$?";
	echo -n "Error caught: ";
	echo "$error $(echo `history | tail -1 | head -1 | cut -d ' ' -f 4-`)" > /tmp/EC.txt;
	cat /tmp/EC.txt;
}

trap error_log ERR
