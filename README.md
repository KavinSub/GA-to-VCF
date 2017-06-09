# GA-to-VCF

File guide
1. converter.py - Actually performs the GA to VCF conversion
2. fetch_metadata.py - Fetches the metadata information 1kGenomes
3. fetch_variant.py - Fetches calls belonging to a callset
4. metadata - json output of fetch_metadata.py

How to use:
1. python fetch_metadata.py - metadata is then written to a file called metadata
2. python fetch_variant.py
3. python converter.py - the vcf data will be output to test.vcf

Todo:
1. Currently the source, reference and phasing fields are hardcoded strings.
2. The metadata is missing the following information
   * contig tags
   * ALT tags
3. The floating point formatting is off, because the input floating point formats will vary themselves.
4. fetch_variant.py currently just gets the data for the first 3 call sets it finds on ga4gh. This should
   be made customizable at some point, and it should be straightforward to implement.