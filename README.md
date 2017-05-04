# GA-to-VCF

File guide
1. converter.py - Actually performs the GA to VCF conversion
2. fetch_metadata.py - Fetches the metadata information 1kGenomes
3. fetch_variant.py - Fetches calls belonging to a callset
4. metadata - json output of fetch_metadata.py

How to use:
1. run fetch_metadata.py - metadata is then written to a file called metadata
2. run fetch_variant.py
   * Currently just the first three variant sets are used on reference 1. This will be customizable later on.
3. run converter.py - the vcf data will be output to test.vcf

Todo:
1. Currently the source, reference and phasing fields are hardcoded strings.
2. The metadata is missing the following information
   * INFO tags: VT, EX_TARGET, MULTI_ALLELIC
   * contig tags
   * ALT tags
3. The quality data is missing from the variants. Currently this is hardcoded to 100.
4. The POS field in the original VCF differs from the outputted POS field. This may just be due to using a different reference.