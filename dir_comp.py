from filecmp import dircmp

def print_diff_files(dcmp):
    # Files exist in both but different
    for name in dcmp.diff_files:
        print "diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right)
    # Files existsonly in left
    for name in dcmp.left_only:
        print "%s only found in %s " % (name, dcmp.left)
    # Names exists in both but types differ
    for name in dcmp.common_funny:
        print "%s found in %s and %s but types differ" % (name, dcmp.left, dcmp.right)
    # Names exists in both but cannot compare
    for name in dcmp.funny_files:
        print "%s found in %s and %s but cannot compare" % (name, dcmp.left, dcmp.right)
        
    # Recursively examine sub dirs
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = dircmp('d:/songs', 'h:/songs')
print_diff_files(dcmp)