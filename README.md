# Handling diag-output data

This is a set of scripts which are intended to be used in conjunction with data collected with [Data-gathering in the Event must-gather Fails](https://access.redhat.com/articles/4971311).  These scripts may need to be aggregated in to other projects.  However, they are useful and I'm not entirely sure where they fit elsewhere.


# Journal Analysis

In situations where you only have a journal it can be challenging to quickly determine if containers are running.  `pod_view.py` parses the journal(s) to provide a view of pod health.  Multiple files can be provided as arguments.

~~~
pod_view.py /path/to/journal
~~~

Multiple journals can be parsed at once to provide a cohesive output.

~~~
pod_view.py `ls *.journal.log`
~~~

To make this a little easier, define the following alias:
~~~
alias diag_output_process_journals='pod_view.py `ls *.journal.log`'
~~~

Change to the directory where `diag_output.tar.gz` has been unpacked and run `diag_output_process_journals`.

# Unpacking container logs

To make this a little easier, define the following alias:
~~~
alias diag_output_unpack_logs='for FILE in `ls *.tar.gz`; do tar xvf $FILE; done'
~~~

Change to the directory where `diag_output.tar.gz` has been unpacked and run `diag_output_unpack_logs`.


# Viewing Container Logs

To make this a little easier, define the following function:
~~~
function diag_output_view_log() {
    SEARCH=$1
    if [ ! -z "$2" ]; then SEARCH="$2_$SEARCH"; fi
    FILES=`ls ./var/log/containers/*$SEARCH*`
    for FILE in $FILES; do echo ===== $FILE; cat $FILE; printf "\n\n"; done | vi -
}
~~~

Syntax:
~~~
diag_output_view_log container-name namespace
~~~

Specifying the namespace is optional.  Additionally, a partial container name can be provided which will result in matching logs being opened at once.  For example:

~~~
diag_output_view_log etcd openshift-etcd
~~~


# Installing

1. Copy `pod_view.py` to `~/.local/bin`
2. Make `pod_view.py` executable
2. Add the content of `bashrc-additions` to your `.bashrc` file
3. Enjoy! or don't ... If you don't, please file issues or PRs or tell me to put this somewhere else.
