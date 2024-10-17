window.BENCHMARK_DATA = {
  "lastUpdate": 1729199200267,
  "repoUrl": "https://github.com/developmentseed/morecantile",
  "entries": {
    "morecantile Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bb213ea0544a0e6224056671e47bec7325a543bd",
          "message": "Merge pull request #160 from developmentseed/feature/add-benchmark\n\nadd benchmark",
          "timestamp": "2024-10-17T22:47:12+02:00",
          "tree_id": "7c1d86809f50b0a33e7f916acf39c7cc40bc57f9",
          "url": "https://github.com/developmentseed/morecantile/commit/bb213ea0544a0e6224056671e47bec7325a543bd"
        },
        "date": 1729198168968,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 27835.938458267672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017434435174240333",
            "extra": "mean: 35.92478124993791 usec\nrounds: 5888"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 27190.417465309398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029412499977205734",
            "extra": "mean: 36.77766261867216 usec\nrounds: 15069"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 27249.58197807611,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020329423375510278",
            "extra": "mean: 36.69781066016201 usec\nrounds: 15966"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26643.22658150052,
            "unit": "iter/sec",
            "range": "stddev: 0.000001992104799157507",
            "extra": "mean: 37.53299161950381 usec\nrounds: 15751"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26012.147536546607,
            "unit": "iter/sec",
            "range": "stddev: 0.000002246285965983132",
            "extra": "mean: 38.4435771246883 usec\nrounds: 15449"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24755.893137511663,
            "unit": "iter/sec",
            "range": "stddev: 0.000002145666813328207",
            "extra": "mean: 40.394422226873246 usec\nrounds: 14883"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 7599.18515262934,
            "unit": "iter/sec",
            "range": "stddev: 0.000012997487183763481",
            "extra": "mean: 131.59305634946887 usec\nrounds: 3780"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 165628.37008686937,
            "unit": "iter/sec",
            "range": "stddev: 5.95158167760805e-7",
            "extra": "mean: 6.037612997552994 usec\nrounds: 76953"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 157629.40712018148,
            "unit": "iter/sec",
            "range": "stddev: 7.726803064542622e-7",
            "extra": "mean: 6.343993917566216 usec\nrounds: 77436"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 158075.76267245348,
            "unit": "iter/sec",
            "range": "stddev: 6.364320456934438e-7",
            "extra": "mean: 6.3260805014876675 usec\nrounds: 76185"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 133440.66227662732,
            "unit": "iter/sec",
            "range": "stddev: 6.199191767111791e-7",
            "extra": "mean: 7.493967602820825 usec\nrounds: 47504"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 124840.96934567855,
            "unit": "iter/sec",
            "range": "stddev: 6.510104949049002e-7",
            "extra": "mean: 8.010190927235184 usec\nrounds: 60489"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 103384.53478221432,
            "unit": "iter/sec",
            "range": "stddev: 7.226376914280621e-7",
            "extra": "mean: 9.672626588750044 usec\nrounds: 54128"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 10429.78059390976,
            "unit": "iter/sec",
            "range": "stddev: 0.00002334284555282665",
            "extra": "mean: 95.87929400776926 usec\nrounds: 5891"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "1dbb5fa5dd1a2a3e945879978c3e936f7f9d6344",
          "message": "add benchmark in docs",
          "timestamp": "2024-10-17T22:51:26+02:00",
          "tree_id": "955422a0c9695300ac609b5a6207acdf347d4586",
          "url": "https://github.com/developmentseed/morecantile/commit/1dbb5fa5dd1a2a3e945879978c3e936f7f9d6344"
        },
        "date": 1729198421361,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 27913.906746128847,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018496082253852282",
            "extra": "mean: 35.824437227464834 usec\nrounds: 7113"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 27256.043926344726,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038042771849057276",
            "extra": "mean: 36.689110228261534 usec\nrounds: 15604"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 27351.332755728756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019320418572744497",
            "extra": "mean: 36.56128967940508 usec\nrounds: 16249"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26691.240814766465,
            "unit": "iter/sec",
            "range": "stddev: 0.000002347806963273008",
            "extra": "mean: 37.46547442061095 usec\nrounds: 15657"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26198.032352728966,
            "unit": "iter/sec",
            "range": "stddev: 0.000002057823788672129",
            "extra": "mean: 38.170805598529356 usec\nrounds: 15468"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 25012.554568666845,
            "unit": "iter/sec",
            "range": "stddev: 0.00000422723314710326",
            "extra": "mean: 39.97992277257026 usec\nrounds: 15163"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 7681.622103516133,
            "unit": "iter/sec",
            "range": "stddev: 0.000005903618807971685",
            "extra": "mean: 130.1808376569666 usec\nrounds: 3739"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 160102.465576479,
            "unit": "iter/sec",
            "range": "stddev: 5.217579070424924e-7",
            "extra": "mean: 6.246000000058164 usec\nrounds: 75104"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 155636.15792707624,
            "unit": "iter/sec",
            "range": "stddev: 5.17274984630616e-7",
            "extra": "mean: 6.4252421372966095 usec\nrounds: 74879"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 157382.49612296972,
            "unit": "iter/sec",
            "range": "stddev: 5.86760529741576e-7",
            "extra": "mean: 6.35394675160481 usec\nrounds: 78162"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 135321.18951175586,
            "unit": "iter/sec",
            "range": "stddev: 6.039978442942694e-7",
            "extra": "mean: 7.38982567037756 usec\nrounds: 64814"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 125607.01929312383,
            "unit": "iter/sec",
            "range": "stddev: 6.494169678927579e-7",
            "extra": "mean: 7.961338511395944 usec\nrounds: 64438"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 103897.79050448934,
            "unit": "iter/sec",
            "range": "stddev: 6.9194280633227e-7",
            "extra": "mean: 9.624843754081477 usec\nrounds: 54043"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 10863.451936572368,
            "unit": "iter/sec",
            "range": "stddev: 0.000004862943424056361",
            "extra": "mean: 92.0517719265134 usec\nrounds: 5906"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b2704d20d53c23fac68a4354b5ca60040642669f",
          "message": "Merge pull request #161 from developmentseed/feature/performance-improvement\n\nPerformance improvement",
          "timestamp": "2024-10-17T23:04:15+02:00",
          "tree_id": "202b38ce0e9e3682db11118d28f19bf367c75cc1",
          "url": "https://github.com/developmentseed/morecantile/commit/b2704d20d53c23fac68a4354b5ca60040642669f"
        },
        "date": 1729199199320,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 24862.11453559257,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019492129950717947",
            "extra": "mean: 40.22184028508119 usec\nrounds: 5754"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 24852.18553495046,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030728462641287322",
            "extra": "mean: 40.23790980449854 usec\nrounds: 14779"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 23683.697060960614,
            "unit": "iter/sec",
            "range": "stddev: 0.000007904259426535646",
            "extra": "mean: 42.223137604996865 usec\nrounds: 15014"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24990.58764421827,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018203211163701935",
            "extra": "mean: 40.015065441302504 usec\nrounds: 15235"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 24725.800513145387,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017323404691663823",
            "extra": "mean: 40.44358440360114 usec\nrounds: 15260"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24728.720114726373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015778154743725443",
            "extra": "mean: 40.438809423237515 usec\nrounds: 15133"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 11510.54950673721,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046125642341575415",
            "extra": "mean: 86.87682542129657 usec\nrounds: 3918"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 247568.9310958904,
            "unit": "iter/sec",
            "range": "stddev: 4.2001181176820506e-7",
            "extra": "mean: 4.039279062899342 usec\nrounds: 76782"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 245528.44881440885,
            "unit": "iter/sec",
            "range": "stddev: 4.048445354124478e-7",
            "extra": "mean: 4.072847789446528 usec\nrounds: 81880"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 245698.17672196857,
            "unit": "iter/sec",
            "range": "stddev: 4.630466337046226e-7",
            "extra": "mean: 4.070034272706864 usec\nrounds: 63695"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 247604.02477760866,
            "unit": "iter/sec",
            "range": "stddev: 4.464137351145614e-7",
            "extra": "mean: 4.038706563425912 usec\nrounds: 83599"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 242333.5174500791,
            "unit": "iter/sec",
            "range": "stddev: 4.568578119479004e-7",
            "extra": "mean: 4.126544320085647 usec\nrounds: 79975"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 241996.71427192705,
            "unit": "iter/sec",
            "range": "stddev: 4.3860826458705846e-7",
            "extra": "mean: 4.132287510632558 usec\nrounds: 78971"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 21826.21730472572,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028660382744233347",
            "extra": "mean: 45.81645944592901 usec\nrounds: 7977"
          }
        ]
      }
    ]
  }
}