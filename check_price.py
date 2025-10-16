
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any,Union
import json
import urllib3
from send_mail import send_email_notification




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url="https://www.homedepot.com/p/DEWALT-20V-Drill-Driver-Kit-DCD771C2/204279858"

QUERY="query productClientOnlyProduct($itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput, $skipSpecificationGroup: Boolean = false, $storeId: String, $isBrandPricingPolicyCompliant: Boolean, $skipFavoriteCount: Boolean = false, $configId: String, $skipPaintDetails: Boolean = true, $zipCode: String, $quantity: Int, $skipInstallServices: Boolean = true, $skipKPF: Boolean = false, $skipSubscribeAndSave: Boolean = false) {\n  product(\n    itemId: $itemId\n    dataSource: $dataSource\n    loyaltyMembershipInput: $loyaltyMembershipInput\n  ) {\n    itemId\n    dataSources\n    identifiers {\n      canonicalUrl\n      brandName\n      itemId\n      modelNumber\n      productLabel\n      storeSkuNumber\n      upcGtin13\n      skuClassification\n      specialOrderSku\n      toolRentalSkuNumber\n      rentalCategory\n      rentalSubCategory\n      upc\n      productType\n      isSuperSku\n      parentId\n      omsThdSku\n      sampleId\n      roomVOEnabled\n      __typename\n    }\n    specificationGroup @skip(if: $skipSpecificationGroup) {\n      specifications {\n        specName\n        specValue\n        __typename\n      }\n      specTitle\n      __typename\n    }\n    availabilityType {\n      discontinued\n      status\n      type\n      buyable\n      __typename\n    }\n    details {\n      description\n      collection {\n        url\n        name\n        collectionId\n        __typename\n      }\n      installation {\n        serviceType\n        leadGenUrl\n        __typename\n      }\n      highlights\n      __typename\n    }\n    media {\n      images {\n        url\n        type\n        subType\n        sizes\n        hotspots {\n          coordinate {\n            xCoordinate\n            yCoordinate\n            __typename\n          }\n          omsIDs\n          __typename\n        }\n        ocrHotspots {\n          coordinate {\n            xCoordinate\n            yCoordinate\n            __typename\n          }\n          omsIDs\n          __typename\n        }\n        altText\n        __typename\n      }\n      video {\n        shortDescription\n        thumbnail\n        url\n        videoStill\n        uploadDate\n        dateModified\n        link {\n          text\n          url\n          __typename\n        }\n        title\n        type\n        videoId\n        longDescription\n        __typename\n      }\n      threeSixty {\n        id\n        url\n        __typename\n      }\n      augmentedRealityLink {\n        usdz\n        image\n        __typename\n      }\n      __typename\n    }\n    pricing(\n      storeId: $storeId\n      isBrandPricingPolicyCompliant: $isBrandPricingPolicyCompliant\n    ) {\n      promotion {\n        dates {\n          end\n          start\n          __typename\n        }\n        type\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        dollarOff\n        percentageOff\n        promotionTag\n        savingsCenter\n        savingsCenterPromos\n        specialBuySavings\n        specialBuyDollarOff\n        specialBuyPercentageOff\n        experienceTag\n        subExperienceTag\n        __typename\n      }\n      value\n      original\n      alternatePriceDisplay\n      alternate {\n        bulk {\n          pricePerUnit\n          thresholdQuantity\n          value\n          __typename\n        }\n        unit {\n          caseUnitOfMeasure\n          unitsOriginalPrice\n          unitsPerCase\n          value\n          __typename\n        }\n        __typename\n      }\n      mapAboveOriginalPrice\n      mapDetail {\n        percentageOff\n        dollarOff\n        mapPolicy\n        mapOriginalPriceViolation\n        mapSpecialPriceViolation\n        __typename\n      }\n      message\n      preferredPriceFlag\n      specialBuy\n      unitOfMeasure\n      conditionalPromotions {\n        promotionId\n        skuItemGroup\n        promotionTags\n        eligibilityCriteria {\n          itemGroup\n          minThresholdVal\n          thresholdType\n          minPurchaseAmount\n          minPurchaseQuantity\n          relatedSkusCount\n          omsSkus\n          __typename\n        }\n        reward {\n          tiers {\n            minThresholdVal\n            thresholdType\n            rewardVal\n            rewardType\n            rewardLevel\n            maxAllowedRewardAmount\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            maxPurchaseQuantity\n            __typename\n          }\n          __typename\n        }\n        dates {\n          start\n          end\n          __typename\n        }\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        experienceTag\n        subExperienceTag\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      clearance {\n        value\n        dollarOff\n        percentageOff\n        unitsClearancePrice\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      ratingsReviews {\n        averageRating\n        totalReviews\n        __typename\n      }\n      __typename\n    }\n    seo {\n      seoKeywords\n      seoDescription\n      __typename\n    }\n    taxonomy {\n      breadCrumbs {\n        label\n        url\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionName\n        refinementKey\n        __typename\n      }\n      brandLinkUrl\n      __typename\n    }\n    dataSource\n    favoriteDetail @skip(if: $skipFavoriteCount) {\n      count\n      __typename\n    }\n    info {\n      hidePrice\n      ecoRebate\n      quantityLimit\n      categoryHierarchy\n      sskMin\n      sskMax\n      unitOfMeasureCoverage\n      wasMaxPriceRange\n      wasMinPriceRange\n      productSubType {\n        name\n        link\n        __typename\n      }\n      replacementOMSID\n      hasVisuallySimilar\n      forProfessionalUseOnly\n      isSponsored\n      sponsoredMetadata {\n        campaignId\n        placementId\n        slotId\n        sponsoredId\n        trackSource\n        __typename\n      }\n      globalCustomConfigurator {\n        customExperience\n        customButtonText\n        customDescription\n        customExperienceUrl\n        customTitle\n        customPosition\n        __typename\n      }\n      augmentedReality\n      sponsoredBeacon {\n        onClickBeacon\n        onViewBeacon\n        onClickBeacons\n        onViewBeacons\n        __typename\n      }\n      customerSignal {\n        previouslyPurchased\n        __typename\n      }\n      isBuryProduct\n      isGenericProduct\n      returnable\n      classNumber\n      hasSubscription\n      isLiveGoodsProduct\n      productDepartment\n      paintBrand\n      dotComColorEligible\n      paintFamily\n      gccExperienceOmsId\n      isInStoreReturnMessageEligible\n      movingCalculatorEligible\n      label\n      bathRenovation\n      recommendationFlags {\n        visualNavigation\n        pipCollections\n        packages\n        ACC\n        collections\n        frequentlyBoughtTogether\n        bundles\n        batItems\n        __typename\n      }\n      minimumOrderQuantity\n      projectCalculatorEligible\n      subClassNumber\n      protectionPlanSku\n      eligibleProtectionPlanSkus\n      hasServiceAddOns\n      consultationType\n      pipCalculator {\n        coverageUnits\n        display\n        publisher\n        toggle\n        defaultAdditionalCoverage\n        additionalCoveragePercentage\n        __typename\n      }\n      __typename\n    }\n    paintDetails(configId: $configId, storeId: $storeId) @skip(if: $skipPaintDetails) {\n      brandLogo\n      colorType\n      rgb {\n        red\n        green\n        blue\n        __typename\n      }\n      colorDisplayName\n      __typename\n    }\n    badges(storeId: $storeId) {\n      endDate\n      label\n      name\n      color\n      creativeImageUrl\n      message\n      timerDuration\n      timer {\n        timeBombThreshold\n        daysLeftThreshold\n        dateDisplayThreshold\n        message\n        __typename\n      }\n      __typename\n    }\n    fulfillment(storeId: $storeId, zipCode: $zipCode, quantity: $quantity) {\n      fulfillmentOptions {\n        fulfillable\n        type\n        services {\n          type\n          locations {\n            isAnchor\n            locationId\n            inventory {\n              isOutOfStock\n              quantity\n              isInStock\n              isLimitedQuantity\n              isUnavailable\n              maxAllowedBopisQty\n              minAllowedBopisQty\n              __typename\n            }\n            curbsidePickupFlag\n            isBuyInStoreCheckNearBy\n            distance\n            state\n            storeName\n            storePhone\n            type\n            storeTimeZone\n            __typename\n          }\n          deliveryTimeline\n          deliveryDates {\n            startDate\n            endDate\n            __typename\n          }\n          deliveryCharge\n          dynamicEta {\n            hours\n            minutes\n            __typename\n          }\n          hasFreeShipping\n          freeDeliveryThreshold\n          totalCharge\n          deliveryMessage\n          earliestDeliveryDate\n          shipFromFastestLocation\n          optimalFulfillment\n          hasSameDayCarDelivery\n          shipFromFastestLocationType\n          sameDayDeliveryCharge\n          __typename\n        }\n        priorityDeliveryOptions {\n          date\n          timeline\n          totalCharge\n          __typename\n        }\n        __typename\n      }\n      anchorStoreStatus\n      anchorStoreStatusType\n      backordered\n      backorderedShipDate\n      bossExcludedShipStates\n      excludedShipStates\n      seasonStatusEligible\n      onlineStoreStatus\n      onlineStoreStatusType\n      fulfillmentBundleMessage\n      sthExcludedShipState\n      bundleComponents {\n        id\n        quantity\n        fulfillmentOptions {\n          type\n          availableFulfillmentTypes\n          __typename\n        }\n        __typename\n      }\n      fallbackMode\n      bossExcludedShipState\n      inStoreAssemblyEligible\n      bodfsAssemblyEligible\n      __typename\n    }\n    installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n      scheduleAMeasure\n      gccCarpetDesignAndOrderEligible\n      __typename\n    }\n    keyProductFeatures @skip(if: $skipKPF) {\n      keyProductFeaturesItems {\n        features {\n          name\n          refinementId\n          refinementUrl\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    bundleFlag\n    sizeAndFitDetail {\n      attributeGroups {\n        attributes {\n          attributeName\n          dimensions\n          __typename\n        }\n        dimensionLabel\n        productType\n        __typename\n      }\n      __typename\n    }\n    subscription @skip(if: $skipSubscribeAndSave) {\n      defaultfrequency\n      discountPercentage\n      subscriptionEnabled\n      __typename\n    }\n    seoDescription\n    bundleSpecificationDetails {\n      parents {\n        parentId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"


HEADERS = {
		"Host": "apionline.homedepot.com",
		"Cookie": "bm_ss=ab8e18ef4e; bm_so=287666D1EA2B45707846A174DAFC2B87A56E60BE89CF32D07B5ECDB70292E376~YAAQFC0tFzVW65WZAQAAYExDswXJzdMrsMScrvMDFt51dK+NWtms0hvCx65ECkWXO1F6ovAEvkw56+cP7LyJ8kELQLK/w3A+S38O2EbfjSzY6oxtwM8xeRz6IHN8YPZz5CzS8w3+rxy6yVu94ukIQNxFLtNZnJNM+6OvxKjtHMgfI4yKH5wqBPB9DQoh1NZP60DBFdlhJxXKp+v491b03EWuQTe6e9983n1G4AMvCEPZpH9tP5+vfJwYd8F7Rui/gI/dLDuFEd25OBGHOPZMyn1b0PNKoUOHYaA6WvTc09PhiT/IyrIGdC54l0ZQLnY6tSvhtkuieovt+Ml4aYQ+I5+jWOF2txEf0p6jg+1KN21VBo4yhLY+GviO+6a0iEeglOyLk+iRmibqI0V2inBK+D783FH6sVzvC8C3KdKGnZ+VvYKlNaM8CX0ZGAbe0KBSJcjPMNt+j0bjWR8umptbadf8; HD_DC=origin; AKA_A2=A; bm_mi=87508AD2880592A8DA9684D4DFE7CD03~YAAQFC0tF4RW65WZAQAA2VtDsx2VGLvQwSUiAPBPSyvKDA843gZy1iIdAIvN6xDJ9vBYo7O2Qp6KxmgCG252B5wdHsWd5jONjUfE65nhzvS01DqTCwlAhpoJmEcWTlFO2sg7f1kx2Ren0I0AC6pRrUVplO2TKe6rhpWT2mRBraEirIuqucgvpfbQpbR15gIbug5j5V63QUmOfowM//49Q3qEGJhHkZLL+7ELImyG2e2CaG01OVyPot6879N3SV12M2XjliUCqKXQsSMtAgwzZullp9m2UKvPuXZye+vhX1dmnWDxNL9/k9YJpL2t9cZTzQ5iA8riDBKi/DQVHUU/QTle+eza0qhwrNI36VU/49yjW/lv8hhAIO5f0Cbi4WLmeUXOmTSb/mJJM21SgnoUnebE2QeHal8R9nI1iI+bg62wZX7ct0DAnRjrDhw4o8rbD6R0G/TSaw==~1; bm_s=YAAQFC0tF4VW65WZAQAA2VtDswS56Fbu+F8ChsD9Yk5VxzDdcDAIjCuv/BnL5bCF8KxfRuk4HQPQrRcVApPN7NRaYpFEvlObLy27fVt78xIuKTvjZ7jih2jUx2HsAWrvYJ+s1iWssCMbOPmG2zce39CJxF/9kDxufpM8ckiHARDXaG7VOuMjsaY+vYo+6nbv4EAWv37+bG3na1dFx2/7ZDj+SWEdWbYh+T4Wu2dvW04dEUNq5z7O6eXZrhmbsPrZ6ZmXtoO09D9+oFUgrSSgw1H8Sm1rmgfDgbl/UXM5dJki6p3tWj5XmRikxvuTYG9tFqAZHhlLrAtHy8mT3yWwppB9AKNv+DbnfBvPceSBDcIYna7Brqon27Yaw0Bi1MEXOgKVJ2cT0fNbJF6Cb0IUkeS8uPq5ASJCCEClXLVJO0UCH+x07nchcyeVXrORuXysQirx3cRKzyaU27QYWyl+9vyYaZJdbky9B2EZKwl2HmMHC6Yy6msxLy6HlmFv+EIXVWRmsMKvOgItVZiGGY8Q0z1Ed6ekujKwg4DXPfgSD1l24d+g6nmoOOIdhw==; bm_sc=3~1~886605162~YAAQFC0tF4ZW65WZAQAA2VtDswVcU3ISr8CoVoH6wtbiSCXAeRM9jaXtxT//8EshUYTSvyvq2TdgNXD4Zve0yLoXFIfL3+ne6eWuFY4us9Hs2Z60NdLli20GzJVY60phHZ8hOIotyBERjK6ZFpHY+MKNAiUpE+QmVeJDBkh/bYCnYyeeyzZWB7Hncd4kqdtk6PsNYEOZ4tfjVNIpbZEiiFyKHPTj7FCVLA//SrTfbMdDGXSQ2zkVvNwYmboDren2PioCt4YKWYIwdxBBUQN0/VBbO0l9oVreoW0nkhz0/ZD0SU3m6qXM8eCOa3AY1GqKiPwZ78+jM12tIzx/6G5Jp0izT/WgZLpnErQFyJ6UFJqQLq0mDY3CI8c5GWRnuxfWXgLtSX3d9BGAyV84dek+Y5RKv8DnH6YAGmacMdHa1bWFTcFnqI+fuaV/jDup9jhpSBgR6HJ2h6sZmtbSpcb9px2GXyglhrmiF29jiFO6RE0VHiXRtL6gZJ2w/zjmTbrzpjoVLqb92K4/fcWdSaF8hTm3XgJg4ER3yx7XBaKwD6nNJPw=; bm_sz=52A6A8B2536685081B34742E7F30293E~YAAQFC0tF4dW65WZAQAA2VtDsx0fZJsd1+u9DB725gi5Cg2oARGxOov3tuBimSnnfh/qogLdHmaQO3iCKN9VAVPWiKs0wc5UAcNpD2879A/7ddeFZaboQzB0KWVYNE3t3q8P+pE8GuS9VbJaCwvrVhLvSk1Zp4NLZACek2BEKOK0U0Y1G+MqlCCbIsFwUwzGx4pF28Bs3kwSnDunTc4J0V9sw6NbZT8w1d/sjzsDyDxDFqRKHaTF5X9yR1q6Zjwqpc8C76qPkkQZ9SiKjxKoE+bxOWX+zBj0IQO93lqYX4i4v7VmUOiWRJbTlVBjlp+K8eLvGE9qmrIUUkkh7UXnCbxDy/UjDC/XY0EStaDdpLG5vQ2qef6R7guNJvqDiq4K1C9mZ7O2f55rzl/4lLwuTaYSB6f/~3553593~3425345; THD_NR=1; THD_PERSIST=; THD_SESSION=; THD_CACHE_NAV_SESSION=; THD_CACHE_NAV_PERSIST=; kndctr_F6421253512D2C100A490D45_AdobeOrg_cluster=or2; AMCV_F6421253512D2C100A490D45%40AdobeOrg=MCMID|61870717522731510503141627895950757300; ak_bmsc=7BCA7E90AA28062479441C4F0FE31127~000000000000000000000000000000~YAAQFC0tFwRX65WZAQAAsXFDsx1mK2Kol5iqDgIbv4Tiksq9ZWIkk2o6phzax3T3xZh8JV5JYXqfAikL3QGSm0rpKGldgtHXAgSBwOP/nlIYc+s8wcT+z0VvK4fUmyQrSb0P8pBBtlPACXTD0bmi+RV/36kmIvRke1moNaAgDx182E65qGvCwAZPVMHNdC4p8QtH8vCvqR7aMH0Vag5LAAmxijEDqbAw5oUuKg8bx0JTUX8Euc+J7QTixIlSYOW4IvqNHLLkUtuH7wnPWxrJC1jxpmB5CgwtY2+xvW+c3LoG7aXqL0z9/0BuDRXJDFoGO0Elrncdjk7Q7yfKleLTNw8j2fOnFbz6sYjDKkW9lpEk72008LZvkIGBFJALjJv+u7oC5bI81iIpuiG7U+TaZXHinm0VGiZwzVbMXvdfNGzLgjP+OYApfUEc+/uDbaCTE31envEbpgnDr2+wNUKOZhpCNewagyAWUJ3aKlmcnm1hnjKf3vLxTgnbaYmt0i6zRK5V5MIL5+sOuaUdTwy7tWTYtWSYEbqbRGqd5GHS/lr5Sk0N2+Ie1QLioibjM7vRRf6fkKVa6K+z2vLdnPaociwHfMfb4N0PuMV9kCiDFXN4WeuX4U48p2HDwQ==; kndctr_F6421253512D2C100A490D45_AdobeOrg_identity=CiY2MTg3MDcxNzUyMjczMTUxMDUwMzE0MTYyNzg5NTk1MDc1NzMwMFISCP7ejZqbMxABGAEqA09SMjAA8AGY7I2amzM%3D; x-maa-ttsearch=LangQnReActAgentV1; x-ttsearch=plp_speed_priority; _abck=F16AC9BDCA2FDBC011CBA450B85B03EC~0~YAAQFC0tFxlX65WZAQAAFXdDsw6g7aoEY/ROrfr7NxVB7TiIfxTfGQaVNm8uT0RqiqHBbxKotTJ7KcWGq7c4zKFODwpKxtApR0/EOUQLu2M+Qdvg58GD0sb6h20KIFV0zLzANE1lbvfev7Rfg6zfF2SmfnioZCWwyaHlrjwjjDrjqXT0ZC23pXRApHAn6xZp240gzXUekalAazzKKWeKakohFVERHjqeGYLPSIn8I+oy5TSmjtOoa7zRlIVyUS3DjiKuDlvTYG5n6NmixNgEbqF0z4I6MkUsNWbkNES919DcMXndUf2zmmI3MMs2643ormB/Ys6PBysD/Ho+2Pzb4y6npAPLH28pZ172d7XTy6MFzWaD5jXyJzSTTnV/v0yPSyZT2SEnuMIPgwTV04WPxp9NSy6ccussMeSz1vZ+aTUSzIzGu1dMHo3C4OOM42y3eH8QjpzjSU7PN8BGbg2UwB6YxNw8IWRLLANz2GDM9ZpfIe7xGbknSSaTH6aACEMZSZUWasOcktjKLRs5UqARIlH5J/ySLEbalQFUsKuvFEQIu1UBJ1Waem7ClU5fINN1nimygdhjgwghN3NAl/N1j2+dzSceSgvvB7HN4nC7qsEE+/P0aCKyoAstIyPXImC7Pg1lapvAEuUW03Q=~-1~-1~-1~AAQAAAAE%2f%2f%2f%2f%2f5DFrPhXbOsH6GDVAt2cuBBqWTS1JAGY6BSZE%2fpktUgqFI+NIKW3gmyYrsDib9P4K9abM3obcVGSmu1Yh0tS6R4XGIRrjSbH2jVM~-1; thda.s=3d86ef77-2755-61f6-96d1-cbf833449261; thda.u=3c69d29b-4ade-6f31-1245-4c521d08695f; THD_LOCALIZER=%7B%22WORKFLOW%22%3A%22LOC_HISTORY_BY_IP%22%2C%22THD_FORCE_LOC%22%3A%221%22%2C%22THD_INTERNAL%22%3A%220%22%2C%22THD_LOCSTORE%22%3A%22585%2BWest%20Houston%20-%20Houston%2C%20TX%2B%22%2C%22THD_STRFINDERZIP%22%3A%2277082%22%2C%22THD_STORE_HOURS%22%3A%221%3B8%3A00-20%3A00%3B2%3B6%3A00-22%3A00%3B3%3B6%3A00-22%3A00%3B4%3B6%3A00-22%3A00%3B5%3B6%3A00-22%3A00%3B6%3B6%3A00-22%3A00%3B7%3B6%3A00-22%3A00%22%2C%22THD_STORE_HOURS_EXPIRY%22%3A1759652771%7D; DELIVERY_ZIP=77082; DELIVERY_ZIP_TYPE=DEFAULT",
		                   # <-- replace
		"X-Api-Cookies": '{"tt_search":"plp_speed_priority"}',
		"X-Experience-Name": "fusion-gm-pip-desktop",
		"X-Debug": "false",
		'Sec-Ch-Ua-Platform': '"Windows"',
		"X-Thd-Customer-Token": "",                # empty in your Burp capture
		"Accept-Language": "en-GB,en;q=0.9",
		'Sec-Ch-Ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
		"X-Hd-Dc": "origin",
		"Sec-Ch-Ua-Mobile": "?0",
		"X-Parent-Trace-Id": "548f5d9e6991abf97c98fd3c62842d29/11753067661892890008",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
		"Accept": "*/*",
		"Content-Type": "application/json",
		#"X-Cloud-Trace-Context": "e56cca5f6a3344509259b2d81078c12a/2;o=1",
		"X-Current-Url": "/p/DEWALT-20V-MAX-Cordless-1-2-in-Drill-Driver-2-20V-1-3Ah-Batteries-Charger-and-Bag-DCD771C2/204279858",
		"Origin": "https://www.homedepot.com",
		"Sec-Fetch-Site": "same-site",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Dest": "empty",
		"Referer": "https://www.homedepot.com/",
		"Accept-Encoding": "gzip, deflate, br",
		"Priority": "u=1, i",
		#"Content-Length": content_length,   # set to exact length of our bytes
		}





def fetch_product(
    url: str,
    headers: Dict[str, str],
    body_bytes: bytes,
    method: str = "POST",
    proxy: Optional[str] = "http://127.0.0.1:8080",
    verify: Optional[Union[bool, str]] = False,
    timeout: int = 60,
    max_retries: int = 3,
    backoff_factor: float = 0.3,
    allow_redirects: bool = False,
	) -> Dict[str, Any]:

    # Create session and disable environment proxy settings if you want deterministic behavior:
    s = requests.Session()
    # s.trust_env = False   # uncomment to ignore environment variables like HTTP_PROXY

    # Setup retries for transient errors
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]),  # include POST if safe in your app
        backoff_factor=backoff_factor,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s.mount("https://", adapter)
    s.mount("http://", adapter)

    # Configure proxy if provided
    if proxy:
        s.proxies.update({"http": proxy, "https": proxy})

    s.verify = verify  # can be False, True, or path to CA cert

    req = requests.Request(method, url, headers=headers, data=body_bytes)
    prepped = s.prepare_request(req)

    # Optional: inspect prepared request for debugging (comment out in production)
    # print("Prepared headers:\n", prepped.headers)
    # print("Prepared body length:", len(prepped.body or b""))

    try:
        resp = s.send(prepped, timeout=timeout, allow_redirects=allow_redirects)
    except requests.RequestException as e:
        # network / timeout / connection error
        raise
        return
    except Exception as e:
    	return

    # Basic status handling
    if resp.status_code != 200:
        # you can return resp.text for debugging, or raise a more informative exception
        raise requests.HTTPError(f"Unexpected status {resp.status_code}: {resp.text}", response=resp)

    # Parse JSON safely
    try:
        data = resp.json()
    except ValueError as e:
        raise ValueError(f"Response not valid JSON: {e}; body: {resp.text[:1000]}")

    # Extract the product fields you need (adapt keys to the API shape)
    try:
        product = data["data"]["product"]
        return {
            "itemId": product["itemId"],
            "productLabel": product["identifiers"]["productLabel"],
            "canonicalUrl": product["identifiers"]["canonicalUrl"],
            "price_value": product["pricing"]["value"],
            "raw": data,  # include full payload for callers who want more
        }
    except (KeyError, TypeError) as e:
        # If structure changed, surface the full JSON for debugging
        raise ValueError(f"Unexpected JSON structure: {e}; full_json_keys={list(data.keys())}")








def get_all_store_price(itemId="205143494", stores_file="stores.json", proxy="http://127.0.0.1:8080"):

    baseapi = "https://apionline.homedepot.com/federation-gateway/graphql?opname=productClientOnlyProduct"

    # Load stores safely
    try:
        with open(stores_file, "r", encoding="utf-8") as f:
            stores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading stores file: {e}")
        return []

    all_results = []

    

    i=0
    for store in stores:
        i+=1

        # if i > 100:
            
        #     break

        storeId = store.get("storeId")
        zipcode = store.get("storeZip")

        if not storeId or not zipcode:
            print(f"Skipping invalid store entry: {store}")
            continue

        print(f"[{i}] Checking price for store {storeId} (ZIP: {zipcode})...")

        payload = {
            "operationName": "productClientOnlyProduct",
            "variables": {
                "skipSpecificationGroup": False,
                "skipFavoriteCount": False,
                "skipPaintDetails": True,
                "skipInstallServices": True,
                "skipKPF": False,
                "skipSubscribeAndSave": False,
                "isBrandPricingPolicyCompliant": False,
                "itemId": itemId,
                "storeId": storeId,
                "zipCode": zipcode
            },
            "query": QUERY
        }

        try:
            # Send request via your existing fetch_product() or fallback to requests.post
            result = fetch_product(baseapi, HEADERS, json.dumps(payload).encode("utf-8"),
                                   proxy=proxy, verify=False)
            if not result:
            	print("Cannot connect")
            	return

            # Validate response
            required_keys = ["itemId", "productLabel", "canonicalUrl", "price_value"]
            if not all(k in result for k in required_keys):
                print(f"⚠️ Incomplete data from store {storeId}")
                continue

            # Print summary
            print(f"✅ Store {storeId}: {result['productLabel']} - ${result['price_value']}")

            all_results.append({
                "storeId": storeId,
                "zipCode": zipcode,
                "itemId": result["itemId"],
                "label": result["productLabel"],
                "url": result["canonicalUrl"],
                "price": result["price_value"]
            })


        except Exception as e:
            print(f"❌ Failed for store {storeId}: {e}")
            return str(e)

    # Optionally, save results
    if not all_results:
        print("\n⚠️ No successful results.")
        return []

    


    # --- Analyze price discrepancies ---
    prices = [r["price"] for r in all_results]
    baseline_price = max(prices)  # highest price as reference
    flagged = []

    print(f"\n📊 Baseline price (highest): ${baseline_price:.2f}")
    print("Analyzing for significant drops...")

    for r in all_results:
        price = r["price"]
        drop_amount = baseline_price - price
        drop_percent = (drop_amount / baseline_price) * 100

        if drop_percent >= 30 and drop_amount >= 50:
            r["drop_percent"] = round(drop_percent, 2)
            r["drop_amount"] = round(drop_amount, 2)
            flagged.append(r)
            print(f"🚨 {r['label']} at store {r['storeId']} — ${price:.2f} "
                  f"({drop_percent:.1f}% / ${drop_amount:.2f} off)")

    # Save results
    with open("store_prices.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    if flagged:
	    mailformat = ""
	    for r in flagged:
	        price = r["price"]
	        drop_percent = r["drop_percent"]
	        drop_amount = r["drop_amount"]

	        mailformat += (
	            f"{r['label']} at store {r['storeId']}\n"
	            f"💰 Current Price: ${price:.2f}\n"
	            f"📉 Drop: {drop_percent:.1f}% (${drop_amount:.2f} off)\n\n"
	        )

	    # Save flagged data
	    with open("flagged_drops.json", "w", encoding="utf-8") as f:
	        json.dump(flagged, f, indent=2)

	    print(f"\n✅ Flagged {len(flagged)} significant drops (≥30% and ≥$50).")

	    # Send email notification
	    send_email_notification(mailformat)

    else:
	    print("\nℹ️ No significant drops found.")

    return flagged






# If the highest price is $200,
# and another store sells it for $120, that’s:
# $80 cheaper
# 40% off
# That store gets flagged because it’s more than 30% off and more than $50 cheaper.

#send_email_notification("test mail format")
#get_all_store_price(itemId="205143494")


