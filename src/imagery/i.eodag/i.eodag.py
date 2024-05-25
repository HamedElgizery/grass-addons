#!/usr/bin/env python3

############################################################################
#
# MODULE:      i.landsat.download
# AUTHOR(S):   Hamed Elgizery
# PURPOSE:     Downloads imagery datasets e.g. Landsat, Sentinel, and MODIS
#              using EODAG API.
# COPYRIGHT:   (C) 2024-2025 by Hamed Elgizery, and the GRASS development team
#
#              This program is free software under the GNU General Public
#              License (>=v2). Read the file COPYING that comes with GRASS
#              for details.
#
#############################################################################


# %Module
# % description: Eodag interface to install imagery datasets from various providers.
# % keyword: eodag
# % keyword: sentinel
# % keyword: landsat
# % keyword: modis
# % keyword: datasets
# % keyword: download
# %end

# %option
# % key: dataset
# % type: string
# % description: Imagery dataset to search for
# % required: yes
# % guisection: Filter
# %end

# %option
# % key: provider
# % type: string
# % description: Provider to use for searching/downloading, if none is provided the searching will be done according to the config file priority
# % required: no
# % guisection: Filter
# %end

# %option
# % key: start
# % type: string
# % description: Start date ('YYYY-MM-DD')
# % required: yes
# % guisection: Filter
# %end

# %option
# % key: end
# % type: string
# % description: End date ('YYYY-MM-DD')
# % required: yes
# % guisection: Filter
# %end

# %option
# % key: timeout
# % type: integer
# % description: Download timeout in seconds
# % answer: 300
# % guisection: Optional
# %end

# %flag
# % key: l
# % description: List the search result without downloading
# %end


import sys
import os
import getpass
import grass.script as gs


def main():
    # products: https://github.com/CS-SI/eodag/blob/develop/eodag/resources/product_types.yml

    # TODO: Add option for setting a differnt config file path
    dag = EODataAccessGateway()
    if options["provider"]:
        dag.set_preferred_provider(options["provider"])

    items_per_page = 20
    product_type = options["dataset"]
    start_date = options["start"]
    end_date = options["end"]
    geom = {"lonmin": 1, "latmin": 43, "lonmax": 2, "latmax": 44}
    searh_parameters = {
        "items_per_page": items_per_page,
        "productType": product_type,
        "geom": geom,
        "start": start_date,
        "end": end_date,
        # "cloudCover": cloudcover,
    }
    search_result = dag.search_all(**searh_parameters)
    num_results = len(search_result)
    print(f"Found {num_results} matching scenes " f"of type {product_type}")
    if flags["l"]:
        idx = 0
        for product in search_result:
            print(
                f'Product #{idx} - ID:{product.properties["id"]},provider:{product.provider}'
            )
            idx += 1
    else:
        pass


if __name__ == "__main__":
    options, flags = gs.parser()

    try:
        from eodag import EODataAccessGateway

    except:

        gs.fatal(_("Cannot import eodag. Please intall the library first."))

    sys.exit(main())
